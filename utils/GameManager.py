from random import choice
from datetime import datetime

from models.schemas import Players_in_Match, GameData


class MatchApiProps:
    id: int
    start_match: str
    match_type: int


class GameRoom:
    id: int
    start_match: str
    end_match: str

    players_in_match: list[Players_in_Match] = []
    round: int
    moves = []

    player_turn: int  # index of player in player list
    player_focus: int | None

    def __init__(self, player_cerate_match: Players_in_Match):
        print("Creating Match Room...")
        self.id = 1 # get room id from TinyDB
        print(f"Room id: {self.id}")
        self.players_in_match.append(player_cerate_match)
        self.round = 1
        self.player_turn = 0
        print(f'{self.players_in_match.__len__()} jogadores conectados.')
    
    def gameHandle(self, data: GameData):
        match data.data_type:
            case  "connect":
                self.players_in_match.append(data.player)
                print(f"Player {data.player.id} connected.")
            case "start":
                self.onGameStart()
            
        

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        print(f"Sorteando {number_of_cards} cartas para o jogador {player.id}...")
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


# if __name__ == "__main__":
if True:
    # Criando jogadores
    player1 = Players_in_Match(1, list(range(1, 21)))
    player2 = Players_in_Match(2, list(range(21, 41)))
    player3 = Players_in_Match(4, list(range(41, 61)))

    # Player3 cria a sala do jogo
    game = GameRoom(player3)
    print(game.id)
    
    # Connecting player1
    con_player1 = GameData(data_type='connect', player=player1)
    game.gameHandle(con_player1)

    # Connecting player2
    con_player2 = GameData(data_type='connect', player=player2)
    game.gameHandle(con_player2)

    # Starting the Game
    start_command = GameData(data_type='start')
    game.gameHandle(start_command)
    
    