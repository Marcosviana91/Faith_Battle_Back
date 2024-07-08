from collections import defaultdict
from datetime import datetime
from random import choice, shuffle
from uuid import uuid1

from pydantic import BaseModel
from .players_schema import PlayersInMatchSchema, PlayersSchema


MINIMUM_DECK_CARDS = 10
MAXIMUM_CARDS_REPEATS = 2
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15
MAXIMUM_DECK_TRIES = 3


def _checkDeckCardsRepeats(deck: list) -> list:
    result = []
    keys = defaultdict(list)
    for key, value in enumerate(deck):
        keys[value].append(key)

    for value in keys:
        if len(keys[value]) > MAXIMUM_CARDS_REPEATS:
            result.append(value)
    return result


class RetryCardsSchema:
    player_id: int
    cards_id: list[int]


class MoveSchema:
    match_room_id: int
    match_round: int
    player_move: int
    card_id: str
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive
    player_target: int | None
    card_target: str | None

    def __init__(
        self,
        player_move: int,
        card_id: int,
        move_type: str,
        player_target: int | None = None,
        card_target: int | None = None
    ):
        self.player_move = player_move
        self.card_id = card_id
        self.move_type = move_type
        self.player_target = player_target
        self.card_target = card_target


class RoomSchema(BaseModel):
    id: str = None
    name: str
    created_by: PlayersSchema
    room_stage: int = 0
    
    connected_players: list[PlayersSchema] = []
    max_players: int = 2
    match_type: str = 'survival'
    password: str = None

    __pydantic_post_init__ = 'model_post_init'
    def model_post_init(self, *args, **kwargs):
        self.connect(self.created_by, self.password)
        self.id = uuid1().hex

    def _getPlayerById(self, player_id: int):
        for player in self.connected_players:
            if player_id == player.id:
                return player
        raise IndexError(f'Player with id {player_id} not found')

    def allPlayersIsReady(self) -> bool:
        count = 0
        for player in self.connected_players:
            if player.ready == True:
                count += 1
        if count == len(self.connected_players):
            self.room_stage += 1
            self.setPlayersNotReady()
            return True
        return False

    def setPlayersNotReady(self):
        for player in self.connected_players:
            player.ready = False

    @property
    def getRoomStats(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_by": self.created_by.id,
            "max_players": self.max_players,
            "connected_players": self.getPlayersStats,
            "has_password": bool(self.password),
            "room_stage": self.room_stage,
            "match_type": self.match_type,

        }

    @property
    def getPlayersStats(self):
        __response = []
        for player in self.connected_players:
            __response.append({
                "id": player.id,
                "ready": player.ready,
                "xp_points": player.xp_points
            })
        return __response

    def connect(self, player: PlayersSchema, password: str = None):
        if (self.room_stage != 0):
            raise Exception("players can connect only in stage 0")
        if len(self.connected_players) >= self.max_players:
            raise Exception("the room is full")
        if (bool(self.password)):
            if (self.password != password):
                raise Exception("password not match")
        self.connected_players.append(player)
        return self.getRoomStats

    def disconnect(self, player_id: int):
        player = self._getPlayerById(player_id)
        self.connected_players.remove(player)
        return self.getRoomStats

    def setReady(self, player_id: int):
        player = self._getPlayerById(player_id)
        checkDeckCards_result = _checkDeckCardsRepeats(player.card_deck)
        if checkDeckCards_result.__len__() > 0:
            raise Exception(
                f"Cards {checkDeckCards_result} exceed maximum repeats."
            )
        if player.card_deck.__len__() < MINIMUM_DECK_CARDS:
            raise Exception(
                f"Deck must have at least {MINIMUM_DECK_CARDS} cards."
            )
        player.ready = True

        if self.allPlayersIsReady():
            if self.room_stage == 1:
                for player in self.connected_players:
                    self.giveCard(player, INITIAL_CARDS)

    def setNotReady(self, player_id: int):
        player = self._getPlayerById(player_id)
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            raise Exception("Can't be not ready")
        player.ready = False

    def setDeck(self, player_id: int, deck: list[str]):
        if (self.room_stage != 0):
            raise Exception("deck can change only in stage 0")
        player = self._getPlayerById(player_id)
        player.card_deck = deck

    def giveCard(self, player: PlayersSchema, number_of_cards: int = 1):
        # print(f"Sorteando {number_of_cards} cartas para o jogador {player.id}...")
        count = 0
        while count < number_of_cards:
            card_selected = player.card_deck[0]
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        # print(f"mão: {player.card_hand}\ndeck: {player.card_deck}")

    def retryCard(self, player_id: int, cards: list[str]):
        player = self._getPlayerById(player_id)
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            raise Exception(
                f"Player {player.id} reaches maximum retries"
            )
        for card in cards:
            player.card_hand.remove(card)
            player.card_deck.append(card)
        self.giveCard(player, cards.__len__())
        player.deck_try += 1
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            player.ready = True

    def getMatch(self):
        return MatchSchema(room=self)


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
    def model_post_init(self, *args, **kwargs):
        self.start_match = str(datetime.now())
        self.id = self.room.id
        self.match_type = self.room.match_type
        for player in self.room.connected_players:
            new_player = PlayersInMatchSchema(
                id=player.id, card_deck=player.card_deck, card_hand=player.card_hand, faith_points=MAXIMUM_FAITH_POINTS)
            self.players_in_match.append(new_player)
        del self.room
        self.newRoundHandle()

    @property
    def getMatchStats(self):
        __players_in_match = []
        for player in self.players_in_match:
            __players_in_match.append({
                "id": player.id,
                "card_hand": player.card_hand, # REMOVER
                "card_prepare_camp": player.card_prepare_camp,
                "card_battle_camp": player.card_battle_camp,
                "card_in_forgotten_sea": player.card_in_forgotten_sea,
                "faith_points": player.faith_points,
                "wisdom_points": player.wisdom_points,
                "wisdom_used":  player.wisdom_used
            })

        return {
            "id": self.id,
            "start_match": self.start_match,
            "match_type": self.match_type,
            "round_match": self.round_match,
            "player_turn": self.player_turn,
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
        # O jogador prepara suas jogadas

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        count = 0
        while count < number_of_cards:
            # card_selected = player.card_deck[0]
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)

    # Precisa gerar as cartas independentes
    def moveCard(self, player_id: int, card_id: str, move_from: str, move_to: str):
        print(f"Player {player_id} is moving the card {card_id}: {move_from} => {move_to}")

    def finishTurn(self):
        ...


# class GameSchema(BaseModel):
#     __pydantic_post_init__ = 'model_post_init'
#     data_type: str

#     def __init__(
#         self,
#         data_type: str,
#         player_data: PlayersInMatchSchema | None = None,
#         player_id: int | None = None,
#         room_id: int | None = None,
#         move: MoveSchema | None = None,
#         retry_cards: RetryCardsSchema | None = None
#     ):
#         self.room_id = room_id
#         self.data_type = data_type  # connect, change_deck, retry_cards, move
#         self.player = player_data
#         self.player_id = player_id
#         self.move = move
#         self.retry_cards = retry_cards

