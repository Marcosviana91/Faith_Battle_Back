from datetime import datetime
from random import shuffle

from pydantic import BaseModel

from schemas.cards_schema import CardSchema
from schemas.players_schema import PlayersInMatchSchema
from schemas.rooms_schema import RoomSchema, MAXIMUM_FAITH_POINTS
from utils.Cards import (
    cardListToDict,
    createCardListObjectsByPlayer,
    getCardInListBySlugId,
)
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB

from utils.LoggerManager import Logger


class MoveSchema(BaseModel):
    match_id: str
    round_match: int
    player_move: int
    move_type: str  # move_to_prepare, move_to_battle, retreat_to_prepare, attack, defense, attach, dettach, card_skill, done, change_deck
    card_id: str | None = None
    player_target: int | None = None
    player_target2: int | None = None
    card_target: str | None = None
    card_list: list[CardSchema] | None = []


class FightSchema(BaseModel):
    match_room: 'MatchSchema'
    fight_stage: int | None = 0
    player_attack: PlayersInMatchSchema
    attack_cards: list[CardSchema] | None
    # attack_abilities: list[CardSchema] | None = []

    player_defense: PlayersInMatchSchema
    defense_cards: list[CardSchema] | None = []
    # defense_abilities: list[CardSchema] | None = []

    __pydantic_post_init__ = 'model_post_init'

    def model_post_init(self, *args, **kwargs):
        __temp_cards_attack = []
        for card in self.attack_cards:
            self.defense_cards.append(None)
            cardObj_atk = getCardInListBySlugId(
                card.in_game_id, self.player_attack.card_battle_camp)
            if card.skill_focus_player_id:
                cardObj_atk.skill_focus_player_id = card.skill_focus_player_id
            __temp_cards_attack.append(cardObj_atk)
        self.attack_cards = __temp_cards_attack
        del __temp_cards_attack

    async def attack(self) -> None:
        for card in self.attack_cards:
            await card.onAttack(match=self.match_room)

    async def defense(self, card_list: list[CardSchema]) -> None:
        __temp_cards_defense = []
        for card in card_list:
            if card.slug != 'not-defense':
                cardObj_def = getCardInListBySlugId(
                    card.in_game_id, self.player_defense.card_battle_camp)
                __temp_cards_defense.append(cardObj_def)
                if cardObj_def != None:
                    await cardObj_def.onDefense(match=self.match_room)
            else:
                __temp_cards_defense.append(None)
            self.defense_cards = __temp_cards_defense
        del __temp_cards_defense
        self.fight_stage = 1

    @property
    def getStats(self):
        return {
            "fight_stage": self.fight_stage,
            "player_attack_id": self.player_attack.id,
            "attack_cards": cardListToDict(self.attack_cards),
            "player_defense_id": self.player_defense.id,
            "defense_cards": cardListToDict(self.defense_cards),
        }

    async def fight(self):
        total_damage = 0
        print(f'Uma luta está sendo travada em {self.match_room.id}')
        if (len(self.attack_cards) > len(self.defense_cards)):
            print("Tem mais ataque do que defesa")
        else:
            index = 0
            for card_atk in self.attack_cards:
                card_def = self.defense_cards[index]
                card_atk.status = 'used'
                if (card_def == None):
                    total_damage += card_atk.attack_point
                    print(f'{card_atk.in_game_id} não foi defendido!')
                    await card_atk.hasSuccessfullyAttacked(player_target=self.player_defense, match=self.match_room)
                else:
                    print(f'{card_atk.in_game_id} VS {card_def.in_game_id}')
                    await card_atk.hasNotSuccessfullyAttacked(player=self.player_attack, match=self.match_room)
                    if card_atk.attack_point >= card_def.defense_points:
                        print(f'{card_atk.in_game_id} derrotou {
                            card_def.in_game_id}')
                        await self.match_room.moveCard(
                            self.player_defense, card_def.in_game_id, "battle", "forgotten")
                    if card_def.attack_point >= card_atk.defense_points:
                        print(f'{card_def.in_game_id} derrotou {
                            card_atk.in_game_id}')
                        await self.match_room.moveCard(
                            self.player_attack, card_atk.in_game_id, "battle", "forgotten")
                if card_atk.slug in ['josue']:
                    await card_atk.rmvSkill(match=self.match_room)
                index += 1
        return total_damage


class MatchSchema(BaseModel):
    room: RoomSchema

    id: str = None
    start_match: str = None
    match_type: str = None
    players_in_match: list[PlayersInMatchSchema] = []
    round_match: int = 0
    player_turn: int = 0
    player_focus_id: int = 0
    can_others_move: bool = False
    fight_camp: FightSchema = None  # create and delete on every fight
    end_match: str = None
    move_now: MoveSchema = None

    __pydantic_post_init__ = 'model_post_init'

    def model_post_init(self, *args, **kwargs):
        self.start_match = str(datetime.now().isoformat())
        self.id = self.room.id
        self.match_type = self.room.match_type
        for player in self.room.connected_players:
            shuffle(player.card_deck)
            new_player = PlayersInMatchSchema(
                id=player.id,
                card_deck=createCardListObjectsByPlayer(
                    player.id, player.card_deck),
                card_hand=createCardListObjectsByPlayer(
                    player.id, player.card_hand),
                faith_points=MAXIMUM_FAITH_POINTS
            )
            self.players_in_match.append(new_player)
        shuffle(self.players_in_match)
        del self.room

    def _getPlayerById(self, player_id: int):
        for player in self.players_in_match:
            if player_id == player.id:
                return player
        print(f'_getPlayerById: ID {player_id} not found')
        return None

    async def sendToPlayer(self, data: dict, player_id: int):
        await WS.sendToPlayer(data, player_id)

    async def updatePlayers(self):
        for player in self.players_in_match:
            await self.sendToPlayer(
                {
                    "data_type": "match_update",
                    "match_data": self.getMatchStats
                },
                player.id
            )
            await self.sendToPlayer(
                {
                    "data_type": "player_update",
                    "player_data": player.getPlayerStats(private=True)
                },
                player.id
            )

    @property
    def getMatchStats(self):
        self.__setCardHandStatus()
        __players_in_match = []
        for player in self.players_in_match:
            __players_in_match.append(player.getPlayerStats())

        response = {
            "id": self.id,
            "start_match": self.start_match,
            "match_type": self.match_type,
            "round_match": self.round_match,
            "player_turn": self.players_in_match[self.player_turn].id,
            "player_focus_id": self.player_focus_id,
            "can_others_move": self.can_others_move,
            "players_in_match": __players_in_match
        }
        if (self.fight_camp):
            response.update({
                "fight_camp": self.fight_camp.getStats
            })
        if (self.end_match):
            response.update({
                "end_match": self.end_match
            })
        return response

    async def newRoundHandle(self):
        self.round_match += 1
        for player in self.players_in_match:
            # Reseta as cartas ['daniel', ]
            daniel_card = getCardInListBySlugId(
                'daniel', player.card_battle_camp)
            if daniel_card:
                await daniel_card.rmvSkill()
            if player.wisdom_points < 10:
                player.wisdom_points += 1
                player.wisdom_available += 1
            if self.round_match > 10:
                self.takeDamage(player, 1)
        self.player_turn = 0
        await self.playerTurnHandle()

    async def playerTurnHandle(self):
        player = self.players_in_match[self.player_turn]
        if player.faith_points < 1:
            await self.finishTurn()
        self.player_focus_id = self.players_in_match[self.player_turn].id
        player.wisdom_available = player.wisdom_points
        if (self.round_match == 1 and self.player_turn == 0):
            ...
        else:
            self.giveCard(player)
        for card in player.card_prepare_camp:
            card.status = "ready"
        for card in player.card_battle_camp:
            card.status = "ready"
        await self.sendToPlayer(data={
            "data_type": "notification",
            "notification": {
                "message": "Sua vez de jogar!"
            }
        },
            player_id=player.id)
        # O jogador prepara suas jogadas

    # setar a disponibilidade de uso das cartas de cada jogador
    def __setCardHandStatus(self):
        for player in self.players_in_match:
            for card in player.card_hand:
                card.status = "not-enough" if (card.wisdom_cost >
                                               player.wisdom_available) else "ready"

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        if (len(player.card_deck) == 0):
            return None
        count = 0
        while count < number_of_cards:
            card_selected = player.card_deck[0]
            # card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        return card_selected

    async def moveCard(self, player: PlayersInMatchSchema, card_id: str, move_from: str, move_to: str):
        move_done: bool = True
        print(f"Player {player.id} is trying moving the card {
              card_id}: {move_from} => {move_to}")
        if (move_from == "hand"):
            card = getCardInListBySlugId(card_id, player.card_hand)
            print(card)
            if (move_to == "prepare" and (card.wisdom_cost <= player.wisdom_available)):
                __card_cost = 1
                __card_cost = card.wisdom_cost
                # card.status = "used"  # Precisa ficar antes do card.onInvoke - Sansão
                await card.onInvoke(self)
                player.wisdom_available -= __card_cost
            elif (move_to == 'forgotten'):
                player.card_hand.remove(card)
                player.card_in_forgotten_sea.append(card)
                await card.onDestroy(self)
        if (move_from == "prepare"):
            card = getCardInListBySlugId(card_id, player.card_prepare_camp)
            card.status = "used"
            if (move_to == 'forgotten'):
                player.card_prepare_camp.remove(card)
                player.card_in_forgotten_sea.append(card)
                await card.onDestroy(self)
            elif (move_to == 'battle'):
                player.card_prepare_camp.remove(card)
                player.card_battle_camp.append(card)
                await card.onMoveToAttackZone(self)
        if (move_from == "battle"):
            card = getCardInListBySlugId(card_id, player.card_battle_camp)
            if (move_to == "forgotten"):
                await card.onDestroy(self)
                player.card_battle_camp.remove(card)
                player.card_in_forgotten_sea.append(card)
            if (move_to == "prepare"):
                player.card_battle_camp.remove(card)
                player.card_prepare_camp.append(card)
                card.status = "used"
                await card.onRetreatToPrepareZone(self)
        if bool(move_done):
            print("moveCard Done ")
        return bool(move_done)

    async def beginAttack(self, move: MoveSchema):
        if ((not move.player_target) or (move.player_move == move.player_target)):
            print("Escolha um oponente")
        else:
            print(f'Jogador {move.player_move} está atacando o jogador {
                move.player_target} com as cartas {move.card_list}')
            self.can_others_move = True
            self.player_focus_id = move.player_target
            player_attack = self._getPlayerById(move.player_move)
            player_defense = self._getPlayerById(move.player_target)
            print(f"Sala {self.id} vai criar fight_camp")
            self.fight_camp = FightSchema(
                match_room=self,
                player_attack=player_attack,
                player_defense=player_defense,
                attack_cards=move.card_list,
                defense_cards=[]
            )
            await self.fight_camp.attack()

    async def beginDefense(self, move: MoveSchema):
        print(f'Jogador {move.player_move} está defendendo o ataque do jogador {
            move.player_target} com as cartas {move.card_list}')
        await self.fight_camp.defense(move.card_list)

    async def fightNow(self):
        damage = await self.fight_camp.fight()
        self.takeDamage(self.fight_camp.player_defense, damage)
        self.fight_camp = None

    def takeDamage(self, player: PlayersInMatchSchema, damage: int):
        player.faith_points -= damage
        print(f'Jogador {player.id} perdeu {damage} de fé.')
        if (player.faith_points < 1):
            print(f'Jogador {player.id} morreu.')
        self.checkWinner()

    def checkWinner(self):
        winner: list[PlayersInMatchSchema] = []
        for player in self.players_in_match:
            if player.faith_points > 0:
                winner.append(player)
        if len(winner) == 1:
            print(f'{winner[0].id} venceu')
            self.player_focus_id = winner[0].id
            return True
        return False

    # Durante o jogo a comunicação será (em maior parte) para movimentação

    async def incoming(self, data: dict):
        Logger.info(f'>>> {data}', 'MATCH')
        move = MoveSchema(**data)
        assert self.id == move.match_id
        assert self.round_match == move.round_match
        self.move_now = move
        player = self._getPlayerById(move.player_move)
        if move.move_type == 'move_to_prepare':
            await self.moveCard(player, card_id=move.card_id,
                                move_from="hand", move_to="prepare")
        if move.move_type == 'done':
            await self.finishTurn()
        if move.move_type == 'move_to_battle':
            await self.moveCard(player, card_id=move.card_id,
                                move_from="prepare", move_to="battle")
        if move.move_type == 'retreat_to_prepare':
            await self.moveCard(player, card_id=move.card_id,
                                move_from="battle", move_to="prepare")
        if move.move_type == 'attack':
            await self.beginAttack(move)
        if move.move_type == 'defense':
            await self.beginDefense(move)
        if move.move_type == 'fight':
            await self.fightNow()
        if move.move_type == 'surrender':
            print(f'{player.id} SURRENDERED...')
            if player.id == self.player_focus_id:
                await self.finishTurn()
            self.takeDamage(player, player.faith_points)
            DB.setPlayerInRoom(player_id=player.id, room_id="")
        if move.move_type == 'change_deck':
            self._reorderPlayerDeck(player, new_deck=move.card_list)
        if move.move_type == 'card_skill':
            card = getCardInListBySlugId(
                card_slug=move.card_id, card_list=player.card_prepare_camp)
            await card.addSkill(match=self)
        if move.move_type == 'attach':
            card = getCardInListBySlugId(
                card_slug=move.card_id, card_list=player.card_prepare_camp)
            await card.onAttach(match=self)
        if move.move_type == 'dettach':
            card = getCardInListBySlugId(
                card_slug=move.card_id, card_list=player.card_prepare_camp)
            await card.onDettach(match=self)
        self.move_now = None
        await self.updatePlayers()

    def _reorderPlayerDeck(self, player: PlayersInMatchSchema, new_deck: list[CardSchema]):
        for card in new_deck[::-1]:
            _card = getCardInListBySlugId(card.in_game_id, player.card_deck)
            player.card_deck.remove(_card)
            player.card_deck.insert(0, _card)

    async def finishTurn(self):
        if (self.player_turn < len(self.players_in_match)-1):
            self.player_turn += 1
            await self.playerTurnHandle()
        else:
            await self.newRoundHandle()
