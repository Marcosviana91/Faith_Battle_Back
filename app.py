from utils import GameRoom
from models.schemas import Players_in_Match, GameData, Move

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
    
    ## ROUND 1
    
    # Player4 moves first card to prepare zone
    move_4 = Move(player_move=player4.id, card_id=player4.card_hand[0], move_type='move_to_prepare')
    move_player4 = GameData(data_type='move', player_id=player4.id, move=move_4)
    game.gameHandle(move_player4)
    
    # Player4 finishes their tunr
    finish_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(finish_player4)
    
    # Player7 moves last card to prepare zone
    move_7 = Move(player_move=player7.id, card_id=player7.card_hand[-1], move_type='move_to_prepare')
    move_player7 = GameData(data_type='move', player_id=player7.id, move=move_7)
    game.gameHandle(move_player7)
    
    # Player7 finishes their tunr
    finish_player7 = GameData(data_type='ready', player_id=player7.id)
    game.gameHandle(finish_player7)
    
    # Player2 moves last card to prepare zone
    move_2 = Move(player_move=player2.id, card_id=player2.card_hand[-1], move_type='move_to_prepare')
    move_player2 = GameData(data_type='move', player_id=player2.id, move=move_2)
    game.gameHandle(move_player2)
    
    # Player2 finishes their tunr
    finish_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(finish_player2)
    
    ## ROUND 2
    
