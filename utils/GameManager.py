from random import choice
from datetime import datetime

from models.schemas import Players_in_Match, GameData

from pprint import pprint

from collections import defaultdict

MINIMUM_DECK_CARDS = 10

def checkDeckCardsRepeats(deck: list) -> list:
    result = []
    keys = defaultdict(list)
    for key, value in enumerate(deck):
        keys[value].append(key)

    for value in keys:
        if len(keys[value]) > 2:
            result.append(value)
    return result


class GameRoom:
    id: int
    start_match: str
    end_match: str

    # Stages
    #   0: players has connecteds, check decks
    #   1: cards in hand ok
    #   2: game in curse
    game_stage: int

    players_in_match: list[Players_in_Match] = []
    round: int
    moves = []

    player_turn: int  # index of player in player list
    player_focus: int | None

    def __init__(self, player_cerate_match: Players_in_Match):
        print("Creating Match Room...")
        self.id = 1  # get room id from TinyDB
        print(f"Room id: {self.id}")
        self.game_stage = 0
        self.players_in_match.append(player_cerate_match)
        self.round = 0
        self.player_turn = 0

    def getPlayerIndexByPlayerId(self, player_id: int) -> int:
        for player in self.players_in_match:
            if player.id == player_id:
                return self.players_in_match.index(player)
        raise IndexError(f'Player with id {player_id} not found')

    def allPlayersIsReady(self) -> bool:
        count = 0
        for player in self.players_in_match:
            if player.ready == True:
                count += 1
        return count == len(self.players_in_match)

    def setPlayersNotReady(self):
        for player in self.players_in_match:
            player.ready = False

    def gameHandle(self, data: GameData):
        match data.data_type:
            case  "connect":
                self.players_in_match.append(data.player)
                print(f"Player {data.player.id} connected.")
            case  "disconnect":
                self.players_in_match.remove(data.player)
                print(f"Player {data.player.id} disconnected.")
            case "ready":
                player_index = self.getPlayerIndexByPlayerId(data.player_id)
                # Checando se o deck está ok
                checkDeckCards_result = checkDeckCardsRepeats(self.players_in_match[player_index].card_deck)
                if checkDeckCards_result.__len__() > 0:
                    print(f"Player {data.player_id} is not ready due cards {checkDeckCards_result} exceed maximum repeats")
                elif self.players_in_match[player_index].card_deck.__len__() < MINIMUM_DECK_CARDS:
                    print(f"Player {data.player_id} is not ready due their deck has less than 30 cards")
                else:
                    self.players_in_match[player_index].ready = True
                    print(f"Player {data.player_id} is ready.")
                if self.allPlayersIsReady():
                    print(f"All players is ready")
                    self.game_stage += 1
                    self.setPlayersNotReady()
            case "unready":
                player_index = self.getPlayerIndexByPlayerId(data.player_id)
                self.players_in_match[player_index].ready = False
                print(f"Player {data.player_id} is not ready.")
            case "change_deck":
                player_index = self.getPlayerIndexByPlayerId(data.player.id)
                self.players_in_match[player_index].card_deck = data.player.card_deck
                print(f"Player {data.player.id} has change their deck.")

            case "start":
                # self.onGameStart()
                print(f'{self.players_in_match.__len__()} players connecteds.')
                # for player in self.players_in_match:
                #     pprint(player.model_dump(), depth=1)

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        print(f"Sorteando {number_of_cards} cartas para o jogador {
              player.id}...")
        count = 0
        while count < number_of_cards:
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        print(f"mão: {player.card_hand}\ndeck: {player.card_deck}")

    def onGameStart(self):
        print("Starting...")
        self.start_match = datetime.now()
        for player in self.players_in_match:
            self.giveCard(player, 5)

    def playerTurnHandle(self):
        ...
