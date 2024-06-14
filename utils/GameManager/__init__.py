from random import choice
from datetime import datetime

from models.schemas import Players_in_Match, GameData, GameRoomSchema

from pprint import pprint

from .stages import stage0


class GameRoom(GameRoomSchema):


    def __init__(self, player_cerate_match: Players_in_Match):
        print("Creating Match Room...")
        self.id = 1  # get room id from TinyDB
        print(f"Room id: {self.id}")
        self.game_stage = 0
        self.players_in_match.append(player_cerate_match)
        self.round = 0
        self.player_turn = 0

    def getPlayerByPlayerId(self, player_id: int) -> Players_in_Match:
        for player in self.players_in_match:
            if player.id == player_id:
                return player
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
        match self.game_stage:
            case 0:
                stage0.dataHandle(self, data)
            case 1:
                print('Stage to sort cards and retry the sort')
                match data.data_type:
                    case  "retry":
                        print('Retry')
                        player = self.getPlayerByPlayerId(data.player_id)
                        self.retryCard(player, data.retry_cards)

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        '''
        Give to player a number of cards
        @ Params:
            player : Players_in_Match
            number_of_cards : int = 1
        @ Return None
        '''
        print(f"Sorteando {number_of_cards} cartas para o jogador {player.id}...")
        count = 0
        while count < number_of_cards:
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        print(f"mão: {player.card_hand}\ndeck: {player.card_deck}")
    
    def retryCard(self, player: Players_in_Match, cards: list):
        print(f'Retring {cards.__len__()} cards to player {player.id}')
        count = 0
        self.giveCard(player, cards.__len__())

    def onGameStart(self):
        print("Starting...")
        self.start_match = datetime.now()
        for player in self.players_in_match:
            self.giveCard(player, 5)

    def playerTurnHandle(self):
        ...
