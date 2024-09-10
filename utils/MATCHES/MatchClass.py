from datetime import datetime
from zoneinfo import ZoneInfo
from random import shuffle
from typing import List, TYPE_CHECKING, Dict

from fastapi import WebSocket

from utils.ConnectionManager import WS

from utils.LoggerManager import Logger
# from utils.console import consolePrint

from utils.Cards.standard.base_cards import C_Card_Match, cardListToDict, getCardInListBySlugId
from utils.Cards import createCardMatchByCardList

if TYPE_CHECKING:
    from utils.ROOM.RoomClass import C_Room, C_Player


class C_Player_Match:
    def __init__(self, id: int):
        self.id = id

        self.card_deck: list[C_Card_Match] = []
        self.card_hand: list[C_Card_Match] = []
        self.card_prepare_camp: list[C_Card_Match] = []
        self.card_battle_camp: list[C_Card_Match] = []
        self.card_in_forgotten_sea: list[C_Card_Match] = []

        self.faith_points: int = 0
        self.wisdom_points: int = 0
        self.wisdom_available: int = 0

        # lista de ids que já foi atacado, para não se repetir
        self.ja_atacou: list[int] = []
        self.fe_inabalavel: bool = False  # não pode perder pontos de fé
        self.incorruptivel: bool = False  # não pode ser alvo de pecados
        # não pode sofrer dano de efeitos de cartas como Davi
        self.nao_sofre_danos_de_efeitos: bool = False
        self.nao_sofre_ataque_de_herois: bool = False  # não pode ser atacado por heróis

    def getStats(self, private: bool = False):

        _data = {
            'id': self.id,
            'card_deck': cardListToDict(self.card_deck),  # remover futuramente
            "card_prepare_camp": cardListToDict(self.card_prepare_camp),
            "card_battle_camp": cardListToDict(self.card_battle_camp),
            "card_in_forgotten_sea": cardListToDict(self.card_in_forgotten_sea),
            "faith_points": self.faith_points,
            "wisdom_points": self.wisdom_points,
            "wisdom_available":  self.wisdom_available,
            "fe_inabalavel": self.fe_inabalavel,
            "incorruptivel": self.incorruptivel,
            "nao_sofre_danos_de_efeitos": self.nao_sofre_danos_de_efeitos,
            "nao_sofre_ataque_de_herois": self.nao_sofre_ataque_de_herois,
        }

        if private:
            _data.pop('card_prepare_camp')
            _data.pop('card_battle_camp')
            _data.pop('card_in_forgotten_sea')
            _data.update(
                {
                    'card_hand': cardListToDict(self.card_hand),
                    "ja_atacou": self.ja_atacou,
                }
            )

        return _data


class MoveSchema:
    def __init__(self,
                 player_move: int, move_type: str,
                 card_id: str | None = None,
                 player_target_id: int | None = None,
                 player_target2_id: int | None = None,
                 card_target_id: str | None = None,
                 card_list: List[Dict] | None = [],
                 *args, **kwargs
                 ) -> None:
        self.player_move_id = player_move  # jogador da vez
        # move_to_prepare, move_to_battle, retreat_to_prepare, attack, defense, attach, dettach, card_skill, done, change_deck
        self.move_type = move_type
        self.card_id = card_id
        self.player_target_id = player_target_id
        self.player_target2_id = player_target2_id
        self.card_target_id = card_target_id
        self.card_list = card_list


class FightSchema:
    def __init__(
        self,
        match_room: 'C_Match',
        player_attack: C_Player_Match,
        player_defense: C_Player_Match,
        attack_cards: List[Dict],
    ):
        self.fight_stage: int = 0
        self.match_room = match_room

        self.player_attack = player_attack
        self.attack_cards: list[C_Card_Match] | None
        # attack_abilities: list[C_Card_Match] | None = []

        self.player_defense = player_defense
        self.defense_cards: list[C_Card_Match] | None = []
        # defense_abilities: list[C_Card_Match] | None = []

        __temp_cards_attack = []
        for card in attack_cards:
            self.defense_cards.append(None)
            cardObj_atk = getCardInListBySlugId(
                card['in_game_id'], self.player_attack.card_battle_camp)
            if card.get('skill_focus_player_id', None):
                cardObj_atk.skill_focus_player_id = card['skill_focus_player_id']
            __temp_cards_attack.append(cardObj_atk)
        self.attack_cards = __temp_cards_attack
        del __temp_cards_attack
        Logger.info(msg=f'Uma batalha iniciou da sala: {self.match_room.id}', tag='C_Match')
        Logger.status(msg=f'{self.getStats()}', tag='FightSchema')

    async def attack(self) -> None:
        for card in self.attack_cards:
            await card.onAttack(match=self.match_room)

    async def defense(self, card_list: List[Dict]) -> None:
        __temp_cards_defense = []
        for card in card_list:
            if card.get('slug') != 'not-defense':
                cardObj_def = getCardInListBySlugId(
                    card.get('in_game_id'), self.player_defense.card_battle_camp)
                __temp_cards_defense.append(cardObj_def)
                if cardObj_def != None:
                    await cardObj_def.onDefense(match=self.match_room)
            else:
                __temp_cards_defense.append(None)
            self.defense_cards = __temp_cards_defense
        del __temp_cards_defense
        self.fight_stage = 1

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
        if (len(self.attack_cards) > len(self.defense_cards)):
            print("Tem mais ataque do que defesa")
        else:
            for index, card_atk in enumerate(self.attack_cards):
                card_def = self.defense_cards[index]
                card_atk.status = 'used'
                if (card_def == None):
                    total_damage += card_atk.attack_point
                    await card_atk.hasSuccessfullyAttacked(player=self.player_attack, match=self.match_room, player_target=self.player_defense)
                else:
                    # temp stores defeated cards
                    _temp_array: List['C_Card_Match'] = []
                    print(f'{card_atk.in_game_id} VS {card_def.in_game_id}')
                    Logger.info(msg=f'{card_atk.in_game_id} VS {card_def.in_game_id}.', tag='FightSchema')
                    Logger.status(msg=f'Carta atacante: {card_atk.getStats()}.', tag='C_Card_Match')
                    Logger.status(msg=f'Carta defensora: {card_def.getStats()}.', tag='C_Card_Match')
                    await card_atk.hasNotSuccessfullyAttacked(player=self.player_attack, match=self.match_room, player_target=self.player_defense)
                    if card_atk.attack_point >= card_def.defense_point:
                        Logger.info(msg=f'{card_atk.in_game_id} derrotou {card_def.in_game_id}.', tag='FightSchema')
                        _temp_array.append(card_def)
                    if card_def.attack_point >= card_atk.defense_point:
                        Logger.info(msg=f'{card_def.in_game_id} VS {card_atk.in_game_id}.', tag='FightSchema')
                        _temp_array.append(card_atk)
                    for _card in _temp_array:
                        _player_id = int(_card.in_game_id.split("_")[0])
                        if _player_id == self.player_attack.id:
                            await self.match_room.moveCard(
                                self.player_attack, card_atk.in_game_id, "battle", "forgotten")
                        elif _player_id == self.player_defense.id:
                            await self.match_room.moveCard(
                                self.player_defense, card_def.in_game_id, "battle", "forgotten")
        for card_atk in self.attack_cards:
            if card_atk.slug in ['josue']:
                await card_atk.rmvSkill(match=self.match_room)
        self.player_attack.ja_atacou.append(self.player_defense.id)
        return total_damage


def convert_C_Player_and_C_Cards(player: 'C_Player') -> 'C_Player_Match':
    new_player = C_Player_Match(id=player.id)
    new_player.card_hand = createCardMatchByCardList(
        card_list=player.card_hand)
    new_player.card_deck = createCardMatchByCardList(
        card_list=player.card_deck)
    return new_player


class C_Match:
    def __init__(self, room: 'C_Room'):
        self.id = room.id
        self.name = room.name
        self.allow_spectators = room.allow_spectators
        self.spectators = [WebSocket]  # Conexões anônimas de espectadores
        # Tranformar C_Player em C_Player_Match e C_Cards em C_Card_Match
        self.players_in_match: List[List[C_Player_Match]] = []
        for _team_index, _team in enumerate(room.connected_players):
            self.players_in_match.append([])
            for player in _team:
                self.players_in_match[_team_index].append(
                    convert_C_Player_and_C_Cards(player))
        self.faith_points = room.faith_points
        self.deatmatch = room.deatmatch
        self.start_match = str(datetime.now(tz=ZoneInfo("America/Sao_Paulo")))
        self.round_match = 0
        self.team_turn = 0
        self.player_turn = 0

        self.fight_camp: FightSchema = None  # create and delete on every fight
        self.move_now: MoveSchema = None
        self.end_match: str = None
        
        self.winner: int = None
        self.montou_a_armadura_completa: bool = False
        self.first_blood: int = None # derrotou o primeiro herói
        self.has_sins: List[int] = [] # ids de quem usou pecado
        self.take_damage: List[int] = [] # ids de quem tomou dano na fé
        self.not_believe: List[int] = [] # ids de quem usou artefatos equipáveis em heróis no campo de batalha
        
        Logger.info(msg=f'Sala iniciada: {self.id}', tag='C_Match')
        Logger.status(msg=f'{self.getStats()}', tag='C_Match')

        if len(self.players_in_match) > 1:
            shuffle(self.players_in_match)

        for _team in self.players_in_match:
            shuffle(_team)
            for _player in _team:
                _player.faith_points = self.faith_points
                shuffle(_player.card_deck)

    # setar a disponibilidade de uso das cartas de cada jogador
    def __setCardHandStatus(self):
        for _team in self.players_in_match:
            for player in _team:
                for card in player.card_hand:
                    card.status = "not-enough" if (card.wisdom_cost >
                                                   player.wisdom_available) else "ready"

    def getStats(self):
        __players_in_match: List[List[dict]] = []
        for index, _team in enumerate(self.players_in_match):
            __players_in_match.append([])
            for player in _team:
                __players_in_match[index].append(player.getStats())
        if (self.end_match is not None):
            return {
                "id": self.id,
                "start_match": self.start_match,
                "end_match": self.end_match,
                "round_match": self.round_match,
                "players_in_match": __players_in_match,
            }
        self.__setCardHandStatus()
        response = {
            "id": self.id,
            "start_match": self.start_match,
            "round_match": self.round_match,
            "player_turn": self.players_in_match[self.team_turn][self.player_turn].id,
            "players_in_match": __players_in_match,
            'deatmatch': self.deatmatch
        }
        if (self.fight_camp):
            response.update({
                "fight_camp": self.fight_camp.getStats()
            })
        return response

    def _getPlayerById(self, player_id: int):
        for _team in self.players_in_match:
            for _player in _team:
                if _player.id == int(player_id):
                    return _player

    async def sendToPlayer(self, player_id: int, data: dict):
        await WS.sendToPlayer(data, player_id)

    async def updatePlayers(self):
        Logger.status(msg=f'{self.id }<<<: {self.getStats()}', tag='C_Match')
        for _team in self.players_in_match:
            for player in _team:
                Logger.status(msg=f'Jogador: {player.id }<<<: {player.getStats(private=True)}', tag='C_Player_Match')
                await self.sendToPlayer(
                    player.id,
                    {
                        "data_type": "match_update",
                        "match_data": self.getStats()
                    },
                )
                await self.sendToPlayer(
                    player.id,
                    {
                        "data_type": "player_update",
                        "player_data": player.getStats(private=True)
                    },
                )

    async def newRoundHandle(self):
        self.round_match += 1
        for _team in self.players_in_match:
            for player in _team:
                # Reseta as cartas ['daniel', ]
                daniel_card = getCardInListBySlugId(
                    'daniel', player.card_battle_camp)
                if daniel_card:
                    await daniel_card.rmvSkill(match=self)
                if player.wisdom_points < 10:
                    player.wisdom_points += 1
                    player.wisdom_available += 1
                if self.round_match > 10:
                    if self.deatmatch:
                        # Cada jogar perde um ponto de fé a cada rodada
                        self.takeDamage(player, 1)
                        Logger.info(
                            msg=f'Deathmatch - Round {self.round_match}', tag='C_Match')
                    else:
                        # Finaliza a partida
                        ...
        self.team_turn = 0
        self.player_turn = 0
        await self.playerTurnHandle()

    async def playerTurnHandle(self):
        # Manipular a vez de cada jogador de cada time
        player = self.players_in_match[self.team_turn][self.player_turn]
        Logger.info(msg=f'Turno do jogador: {player.id}', tag='C_Match')
        Logger.status(msg=f'{player.getStats()}', tag='C_Player_Match')
        if player.faith_points < 1:
            await self.finishTurn()
        player.wisdom_available = player.wisdom_points
        player.ja_atacou = []
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

    async def finishTurn(self):
        if (self.team_turn < len(self.players_in_match)-1):
            self.team_turn += 1
            await self.playerTurnHandle()
        else:
            self.team_turn = 0
            if (self.player_turn < len(self.players_in_match[0])-1):
                self.player_turn += 1
                await self.playerTurnHandle()
            else:
                await self.newRoundHandle()

    def giveCard(self, player: C_Player_Match, number_of_cards: int = 1):
        if (len(player.card_deck) == 0):
            return None
        count = 0
        while count < number_of_cards:
            card_selected = player.card_deck[0]
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
            Logger.info(msg=f'Jogador: {player.id} comprou a carta: {card_selected.in_game_id}', tag='C_Player_Match')
        return card_selected

    async def moveCard(self, player: C_Player_Match, card_id: str, move_from: str, move_to: str):
        move_done: bool = True
        if (move_from == "hand"):
            card = getCardInListBySlugId(card_id, player.card_hand)
            if (move_to == "prepare" and (card.wisdom_cost <= player.wisdom_available)):
                # card.status = "used"  # Precisa ficar antes do card.onInvoke - Sansão
                await card.onInvoke(self)
            elif (move_to == 'forgotten'):
                player.card_hand.remove(card)
                player.card_in_forgotten_sea.append(card)
                await card.onDestroy(self)
        if (move_from == "prepare"):
            card = getCardInListBySlugId(card_id, player.card_prepare_camp)
            if (move_to == 'battle'):
                await card.onMoveToBattleZone(self)
            elif (move_to == 'forgotten'):
                player.card_prepare_camp.remove(card)
                player.card_in_forgotten_sea.append(card)
                await card.onDestroy(self)
        if (move_from == "battle"):
            card = getCardInListBySlugId(card_id, player.card_battle_camp)
            if (move_to == "forgotten"):
                player.card_battle_camp.remove(card)
                player.card_in_forgotten_sea.append(card)
                await card.onDestroy(self)
            elif (move_to == "prepare"):
                player.card_battle_camp.remove(card)
                player.card_prepare_camp.append(card)
                card.status = "used"
                await card.onRetreatToPrepareZone(self)
        # if bool(move_done):
        #     print("moveCard Done ")
        return bool(move_done)

    async def beginAttack(self, move: MoveSchema):

        Logger.info(msg=f'Jogador: {move.player_move_id} está atacando o jogador {
                    move.player_target_id} com as cartas {move.card_list}', tag='C_Player_Match')
        self.can_others_move = True
        player_attack = self._getPlayerById(move.player_move_id)
        player_defense = self._getPlayerById(move.player_target_id)
        # print(f"Sala {self.id} vai criar fight_camp")
        self.fight_camp = FightSchema(
            match_room=self,
            player_attack=player_attack,
            player_defense=player_defense,
            attack_cards=move.card_list,
        )
        await self.fight_camp.attack()

    async def beginDefense(self, move: MoveSchema):
        Logger.info(msg=f'Jogador: {move.player_move_id} está defendendo o ataque do jogador {
                    move.player_target_id} com as cartas {move.card_list}', tag='C_Player_Match')
        await self.fight_camp.defense(move.card_list)

    async def fightNow(self):
        damage = await self.fight_camp.fight()
        self.takeDamage(self.fight_camp.player_defense, damage)
        self.fight_camp = None

    def takeDamage(self, player: C_Player_Match, damage: int):
        player.faith_points -= damage
        print(f'Jogador {player.id} perdeu {damage} de fé.')
        Logger.info(msg=f'Jogador: {player.id} perdeu {damage}pts de fé.', tag='C_Player_Match')
        if (player.faith_points < 1):
            Logger.info(msg=f'Jogador: {player.id} foi eliminado.', tag='C_Player_Match')
        self.checkWinner()

    def checkWinner(self):
        winner: list[C_Player_Match] = []
        for _team in self.players_in_match:
            for player in _team:
                if player.faith_points > 0:
                    winner.append(player)
        if len(winner) == 1:
            Logger.info(msg=f'Jogador: {player.id} venceu.', tag='C_Match')
            print(f'{winner[0].id} venceu')
            self.winner = winner[0].id # pq?
            # self.player_turn = winner[0].id # pq?
            # Gerar estatisticas...
            return True
        return False

    def _reorderPlayerDeck(self, player: C_Player_Match, new_deck: list[Dict]):
        for card in new_deck[::-1]:
            _card = getCardInListBySlugId(
                card.get('in_game_id'), player.card_deck)
            player.card_deck.remove(_card)
            player.card_deck.insert(0, _card)

    async def finishMatch(self):
        self.end_match = str(datetime.now(tz=ZoneInfo("America/Sao_Paulo")))
        print('preparar a tela de estatísticas')

    async def incoming(self, data: dict):
        Logger.status(msg=f'{self.id }>>>: {data}', tag='C_Match')
        assert self.id == data['match_id']
        assert self.round_match == data['round_match']
        move = MoveSchema(**data)
        self.move_now = move
        player = self._getPlayerById(move.player_move_id)
        if move.move_type == 'move_to_prepare':
            await self.moveCard(player, card_id=move.card_id,
                                move_from="hand", move_to="prepare")

        if move.move_type == 'done':
            await self.finishTurn()

        if move.move_type == 'surrender':
            Logger.info(msg=f'Jogador {player.id} desistiu.', tag='C_Match')
            # if player.id == self.player_turn:
            await self.finishTurn()
            self.takeDamage(player, player.faith_points)
            # DB.setPlayerInRoom(player_id=player.id, room_id="")

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
