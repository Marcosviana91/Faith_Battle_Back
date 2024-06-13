from utils import GameRoom
from models.schemas import Players_in_Match, GameData

from pprint import pprint

if __name__ == "__main__":
    # Criando jogadores
    player1 = Players_in_Match(7, list(range(1, 21)))
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
    
    # Player2 is ready
    ready_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(ready_player2)
    
    # # Player1 change the deck
    # player1 = Players_in_Match(7, [1, 2, 3, 4, 6, 5, 8, 2, 3, 1, 1, 1, 3])
    # change_deck_player1 = GameData(data_type='change_deck', player=player1)
    # game.gameHandle(change_deck_player1)
    
    # Player1 is ready
    ready_player1 = GameData(data_type='ready', player_id=player1.id)
    game.gameHandle(ready_player1)
        
    # # Player2 is not ready
    # ready_player2 = GameData(data_type='unready', player_id=player2.id)
    # game.gameHandle(ready_player2)
    
    # Player3 is ready
    ready_player3 = GameData(data_type='ready', player_id=player3.id)
    game.gameHandle(ready_player3)
    
    # Starting the Game
    start_command = GameData(data_type='start')
    game.gameHandle(start_command)
    
    