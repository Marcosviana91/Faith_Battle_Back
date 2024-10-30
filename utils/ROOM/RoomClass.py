from random import choice
from typing import List

import requests
from nanoid import generate

from utils.Cards.standard.base_cards import C_Card_Room, cardListToDict, getCardInListBySlugId
from utils.Cards.standard.raw_data import STANDARD_CARDS

from utils.DataBaseManager import DB
from utils.console import consolePrint

from settings import env_settings

MINIMUM_DECK_CARDS = 10
MAXIMUM_CARDS_REPEATS = 2
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15
MAXIMUM_DECK_TRIES = 3


class C_Player:
    def __init__(self, id: int, xp_points: int, card_deck: list['C_Card_Room']):
        self.id = id
        self.card_deck = card_deck
        self.xp_points = xp_points

        self.ready: bool = False
        self.deck_try: int = 0
        self.card_hand: list['C_Card_Room'] = []

    def getStats(self, type: str = None):

        _data = {
            'id': self.id,
            'ready': self.ready,
            'xp_point': self.xp_points,
            'deck_try': self.deck_try,
            'card_deck': cardListToDict(self.card_deck),
            'card_hand': cardListToDict(self.card_hand),
        }
        return _data


class C_Room:
    SERVER_AVAILABLE_CARDS = STANDARD_CARDS
    def __init__(
        self,
        name: str,
        max_players: int = 2,
        password: str = "",
        created_by: dict = {},
        *args, **kwargs
    ) -> str:
        self.name = name
        self.max_players = max_players
        self.password = password
        self.id = generate(size=12)
        self.room_stage = 0
        self.connected_players: List[List[C_Player]] = [[]]
        self.created_by = created_by
        # server_settings = requests.get(f'http://{env_settings.DB_HOST}:3111/api/')
        # if server_settings.status_code == 200:
        #     self.SERVER_AVAILABLE_CARDS = server_settings.json()['active_cards']
        #     consolePrint.info("Cartas recebidas do servidor...")
        #     print(self.SERVER_AVAILABLE_CARDS)

        self.setConfig()

    def setConfig(
        self,
        easy_mode: bool = True,
        deatmatch: bool = True,
        allow_spectators: bool = False,
        minimum_deck_cards: int = MINIMUM_DECK_CARDS,
        maximum_cards_repeats: int = MAXIMUM_CARDS_REPEATS,
        faith_points: int = MAXIMUM_FAITH_POINTS,
        initial_cards: int = INITIAL_CARDS,
        maximum_deck_tries: int = MAXIMUM_DECK_TRIES,
    ):
        # Easy mode garante um heroi custo 1 E um artefato ou milagre custo 1
        # Também garante que as cartas trocadas não sejam escolhidas de novo no mesmo momento, mas no próximo sorteio sim
        self.easy_mode = easy_mode
        # Deatmatch permita que a partida se estenda até que o último jogador esteja vivo, após o limite de rodadas, a cada rodada todos perdem 1 ponto de fé
        self.deatmatch = deatmatch
        self.allow_spectators = allow_spectators
        self.minimum_deck_cards = minimum_deck_cards
        self.maximum_cards_repeats = maximum_cards_repeats
        self.faith_points = faith_points
        self.initial_cards = initial_cards
        self.maximum_deck_tries = maximum_deck_tries

        return {
            'easy_mode': self.easy_mode,
            'deatmatch': self.deatmatch,
            'minimum_deck_cards': self.minimum_deck_cards,
            'maximum_cards_repeats': self.maximum_cards_repeats,
            'faith_points': self.faith_points,
            'initial_cards': self.initial_cards,
            'maximum_deck_tries': self.maximum_deck_tries,
        }

    def getStats(self) -> dict:
        _connected_players = []
        for team in self.connected_players:
            _team = []
            for _player in team:
                _team.append(_player.getStats())
            _connected_players.append(_team)

        return {
            'id': self.id,
            'name': self.name,
            'room_stage': self.room_stage,
            'max_players': self.max_players,
            'teams': len(self.connected_players),
            'has_password': bool(self.password),
            'connected_players': _connected_players
        }

    def _getPlayerById(self, player_id: int):
        for team in self.connected_players:
            for player in team:
                if player_id == player.id:
                    return player, team
        # consolePrint.danger(f'Player with id {player_id} not found')

    async def connect(self, player_id: int = None, password: str = None):
        if player_id:
            if player_id and password != self.password:
                return None
        else:
            player_id = self.created_by['id']
        _player_data = await DB.getPlayerById(player_id=player_id)
        selected_deck = _player_data['selected_deck']
        decks = _player_data['decks']
        deck: list['C_Card_Room'] = []
        # for _deck in decks:
        #     if _deck["_id"] == selected_deck:
        #         for card in _deck['cards']:
        #             _new_card = C_Card_Room(card, player_id)
        #             deck.append(_new_card)
        for _card in self.SERVER_AVAILABLE_CARDS:
            _new_card = C_Card_Room(_card, player_id)
            deck.append(_new_card)

        c_player = C_Player(
            id=player_id,
            xp_points=_player_data['xp_points'],
            card_deck=deck
        )
        self.connected_players[0].append(c_player)
        # consolePrint.info(
        #     f'Player {player.id} has Connected in room {self.id}')
        await DB.setPlayerRoomOrMatch(player_id=c_player.id, room_id=self.id)
        return self.getStats()

    async def disconnect(self, player_id: int):
        player = self._getPlayerById(player_id)
        if player:
            player[1].remove(player[0])
            if len(player[1]) == 0:
                self.connected_players.remove(player[1])
            # consolePrint.info(
            #     f'Player {player.id} has disconnected from room {self.id}')
        await DB.setPlayerRoomOrMatch(player_id=player_id)
        return self.getStats

    def setReady(self, player_id: int):
        player = self._getPlayerById(player_id)
        player[0].ready = True
        if self.allPlayersIsReady() and self.room_stage == 1:
            for team in self.connected_players:
                for player in team:
                    self.giveCard(player)

    def allPlayersIsReady(self) -> bool:
        for team in self.connected_players:
            for player in team:
                if player.ready == False:
                    return False
        self.room_stage += 1
        self.setPlayersNotReady()
        return True

    def setPlayersNotReady(self):
        for team in self.connected_players:
            for player in team:
                player.ready = False

    def giveCard(self, player: C_Player, number_of_cards: int = INITIAL_CARDS):
        count = 0
        if self.easy_mode:
            if player.deck_try == 0:
                __heros_1 = []
                __miracles_artifacts_1 = []
                # Por algum motivo que eu desconheço, muitas vezes a EVA não entra na lista
                for card in player.card_deck:
                    if card.wisdom_cost == 1:
                        if card.card_type == 'hero':
                            if card.slug == 'eva':
                                print("ACHOU EVA")
                            __heros_1.append(card)
                        elif card.card_type == 'miracle' or card.card_type == 'artifact':
                            print(card)
                            __miracles_artifacts_1.append(card)
                hero_1_selected = choice(__heros_1)
                print('escolheu', hero_1_selected)
                player.card_hand.append(hero_1_selected)
                player.card_deck.remove(hero_1_selected)
                count += 1
                if len(__miracles_artifacts_1) > 0:
                    miracles_artifacts_1_selected = choice(__miracles_artifacts_1)
                    print('escolheu', miracles_artifacts_1_selected)
                    player.card_hand.append(miracles_artifacts_1_selected)
                    player.card_deck.remove(miracles_artifacts_1_selected)
                    count += 1

        while count < number_of_cards:
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            player.card_deck.remove(card_selected)
            count += 1

    def retryCard(self, player_id: int, cards: List[dict]):
        player = self._getPlayerById(player_id)[0]
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            consolePrint.status(f"Player {player.id} reaches maximum retries")
        else:
            player.deck_try += 1
            if self.easy_mode:
                _temp_array = []
                for card in cards:
                    _card2remove = getCardInListBySlugId(
                        card.get('in_game_id'), player.card_hand)
                    player.card_hand.remove(_card2remove)
                    _temp_array.append(_card2remove)
                self.giveCard(player, len(cards))
                player.card_deck += [*_temp_array]
            else:
                for card in cards:
                    _card2remove = getCardInListBySlugId(
                        card.get('in_game_id'), player.card_hand)
                    player.card_hand.remove(_card2remove)
                    player.card_deck.append(_card2remove)
                self.giveCard(player, len(cards))
        return player
