from random import choice, shuffle
from datetime import datetime

from models.schemas import Players_in_Match, GameData, GameRoomSchema

from .stages import stage0, stage1, stage2


MAXIMUM_FAITH_POINTS = 15

class GameRoom(GameRoomSchema):

    def __init__(self, player_cerate_match: Players_in_Match):
        print("Creating Match Room...")
        self.id = 1  # get room id from TinyDB
        print(f"Room id: {self.id}")
        self.game_stage = 0
        self.players_in_match.append(player_cerate_match)
        self.round = 0
        self.player_turn = 0
        self.can_others_moves = False

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
        if count == len(self.players_in_match):
            self.game_stage += 1
            self.setPlayersNotReady()
            print(f"All players is ready.\nNext stage: stage {
                  self.game_stage}")
            return True
        return False

    def setPlayersNotReady(self):
        for player in self.players_in_match:
            player.ready = False

    def gameHandle(self, data: GameData):
        match self.game_stage:
            case 0:
                stage0.dataHandle(self, data)

            case 1:
                stage1.dataHandle(self, data)

            case 2:
                stage2.dataHandle(self, data)

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        # print(f"Sorteando {number_of_cards} cartas para o jogador {player.id}...")
        count = 0
        while count < number_of_cards:
            card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        # print(f"mão: {player.card_hand}\ndeck: {player.card_deck}")

    def gameStart(self):
        print('Starting game...')
        self.start_match = datetime.now().timestamp()
        for player in self.players_in_match:
            shuffle(player.card_deck)
            player.faith_points = MAXIMUM_FAITH_POINTS
        # shuffle(self.players_in_match)
        self.newRoundHandle()
    
    def newRoundHandle(self):
        self.round += 1
        print(f"ROUND {self.round}. . . . . ")
        # Mais 1 de sabedoria para cada jogador
        for player in self.players_in_match:
            player.wisdom_points += 1
        self.player_turn = 0
        print(self.players_in_match)
        self.playerTurnHandle()
    
    
    def playerTurnHandle(self):
        print(f'Player {self.players_in_match[self.player_turn].id} turn:')
        player = self.players_in_match[self.player_turn]
        player.wisdom_used = 0
        self.giveCard(player, 1)
