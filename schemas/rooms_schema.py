from collections import defaultdict
from random import choice
from nanoid import generate

from pydantic import BaseModel

from schemas.cards_schema import CardSchema
from schemas.players_schema import  PlayersSchema


MINIMUM_DECK_CARDS = 10
MAXIMUM_CARDS_REPEATS = 2
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15
MAXIMUM_DECK_TRIES = 3


def _checkDeckCardsRepeats(deck: list[CardSchema]) -> list:
    result = []
    __list = []
    keys = defaultdict(list)
    for card in deck:
        __list.append(card.slug)
    for key, value in enumerate(__list):
        keys[value].append(key)

    for value in keys:
        if len(keys[value]) > MAXIMUM_CARDS_REPEATS:
            result.append(value)
    return result



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
        if not self.id:
            self.id = generate(size=12)

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
            __response.append(player.getPlayersStats)
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
        if self.room_stage == 0:
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

    def retryCard(self, player_id: int, cards: list[CardSchema]):
        player = self._getPlayerById(player_id)
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            raise Exception(
                f"Player {player.id} reaches maximum retries"
            )
        for card in cards:
            __card2remove = CardSchema(**card)
            player.card_hand.remove(__card2remove)
            player.card_deck.append(__card2remove)
        self.giveCard(player, cards.__len__())
        player.deck_try += 1
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            player.ready = True
        return player

