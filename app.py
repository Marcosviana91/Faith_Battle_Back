from utils import GameRoom
from models.schemas import Players_in_Match, GameData

from pprint import pprint

if __name__ == "__main__":
    # STAGE 0

    # Criando jogadores
    player7 = Players_in_Match(7, list(range(1, 21)))
    player2 = Players_in_Match(2, list(range(21, 41)))
    player4 = Players_in_Match(4, list(range(41, 61)))

    # Player4 cria a sala do jogo
    game = GameRoom(player4)

    # Connecting player7
    con_player7 = GameData(data_type='connect', player=player7)
    game.gameHandle(con_player7)

    # Connecting player2
    con_player2 = GameData(data_type='connect', player=player2)
    game.gameHandle(con_player2)

    # Player2 is ready
    ready_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(ready_player2)

    # # Player7 change the deck
    # player7 = Players_in_Match(7, [1, 2, 3, 4, 6, 5, 8, 2, 3, 1, 1, 1, 3])
    # change_deck_player7 = GameData(data_type='change_deck', player=player7)
    # game.gameHandle(change_deck_player7)

    # Player7 is ready
    ready_player7 = GameData(data_type='ready', player_id=player7.id)
    game.gameHandle(ready_player7)

    # # Player2 is not ready
    # ready_player2 = GameData(data_type='unready', player_id=player2.id)
    # game.gameHandle(ready_player2)

    # Player4 is ready
    ready_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(ready_player4)

    # STAGE 1

    # Player7 1 retry all cards
    retry_player7 = GameData(
        data_type='retry',
        player_id=player7.id,
        retry_cards=[
            *player7.card_hand[:]
        ]
    )
    game.gameHandle(retry_player7)

    # Player7 2 retry first and last cards
    retry_player7 = GameData(
        data_type='retry',
        player_id=player7.id,
        retry_cards=[
            player7.card_hand[0],
            player7.card_hand[-1]
        ]
    )
    game.gameHandle(retry_player7)

    # Player7 3 retry the last cards
    retry_player7 = GameData(
        data_type='retry',
        player_id=player7.id,
        retry_cards=[
            player7.card_hand[0],
        ]
    )
    game.gameHandle(retry_player7)

    # # Player7 4 retry the last cards / Not allowed: raise BaseException
    # retry_player7 = GameData(
    #     data_type='retry',
    #     player_id=player7.id,
    #     retry_cards=[
    #         player7.card_hand[0],
    #     ]
    # )
    # game.gameHandle(retry_player7)

    # # Player7 is not ready
    # ready_player7 = GameData(data_type='unready', player_id=player7.id)
    # game.gameHandle(ready_player7)

    # Player2 is ready
    ready_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(ready_player2)

    # Player4 is ready
    ready_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(ready_player4)
    
    # Stage 2: THE GAME
    
    # # Player4 move
    # move_player4 = GameData(data_type='move', player_id=player4.id)
    # game.gameHandle(move_player4)
