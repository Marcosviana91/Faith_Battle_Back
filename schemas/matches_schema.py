from datetime import datetime
from random import choice, shuffle

from pydantic import BaseModel

from schemas.rooms_schema import RoomSchema
from schemas.players_schema import PlayersInMatchSchema
from utils.Cards import createCardListObjectsByPlayer, cardListToDict
from utils.ConnectionManager import WS


MINIMUM_DECK_CARDS = 10
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15


class MoveSchema(BaseModel):
    match_id: str
    round_match: int
    player_move: int
    card_id: str
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive
    player_target: int | None = None
    card_target: str | None = None


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
    end_match: str = None

    __pydantic_post_init__ = 'model_post_init'

    def __getPlayerById(self, player_id: int):
        for player in self.players_in_match:
            if player_id == player.id:
                return player

    async def updatePlayers(self):
        for player in self.players_in_match:
            await WS.sendToPlayer(
                {
                    "data_type": "match_update",
                    "match_data": self.getMatchStats
                },
                player.id
            )
            await WS.sendToPlayer(
                {
                    "data_type": "player_update",
                    "player_data": {
                        "id": player.id,
                        "card_hand": cardListToDict(player.card_hand),
                        "wisdom_points": player.wisdom_points,
                        "wisdom_used": player.wisdom_used
                    }
                },
                player.id
            )

    def model_post_init(self, *args, **kwargs):
        self.start_match = str(datetime.now().isoformat())
        self.id = self.room.id
        self.match_type = self.room.match_type
        for player in self.room.connected_players:
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
        self.newRoundHandle()

    @property
    def getMatchStats(self):
        __players_in_match = []
        for player in self.players_in_match:
            __players_in_match.append(player.getPlayerStats)

        return {
            "id": self.id,
            "start_match": self.start_match,
            "match_type": self.match_type,
            "round_match": self.round_match,
            "player_turn": self.players_in_match[self.player_turn].id,
            "player_focus_id": self.player_focus_id,
            "can_others_move": self.can_others_move,
            "players_in_match": __players_in_match,
        }

    def newRoundHandle(self):
        self.round_match += 1
        for player in self.players_in_match:
            if player.wisdom_points < 10:
                player.wisdom_points += 1
        self.player_turn = 0
        self.playerTurnHandle()

    def playerTurnHandle(self):
        print(f'Player {self.players_in_match[self.player_turn].id} turn:')
        player = self.players_in_match[self.player_turn]
        player.wisdom_used = 0
        self.giveCard(player)
        # self.updatePlayers()
        # O jogador prepara suas jogadas

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        count = 0
        while count < number_of_cards:
            # card_selected = player.card_deck[0]
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)

    def moveCard(self, player: PlayersInMatchSchema, card_id: str, move_from: str, move_to: str):
        print(f"Player {player.id} is moving the card {
              card_id}: {move_from} => {move_to}")
        for card in player.card_hand:
            if card.in_game_id == card_id:
                player.card_hand.remove(card)
                player.card_prepare_camp.append(card)

    async def incoming(self, data: dict):
        move = MoveSchema(**data)
        print('>>>>> RECV: ', move)
        assert self.id == move.match_id
        assert self.round_match == move.round_match
        player = self.__getPlayerById(move.player_move)
        if move.move_type == 'move_to_prepare':
            self.moveCard(player, card_id=move.card_id, move_from="hand", move_to="prepare")

        await self.updatePlayers()

    def finishTurn(self):
        ...
