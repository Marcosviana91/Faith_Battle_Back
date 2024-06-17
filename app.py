from utils import GameRoom
from models.schemas import Players_in_Match, GameData, Move

from utils.populates.CardPopulate import cardPopulates

# STAGE 0
if __name__ == "__main__":

    GAME_STANDARD_CARDS_SLUGS = [
        'abraao', 'adao', 'daniel',
        'davi', 'elias', 'ester',
        'eva', 'jaco', "jose-do-egito",
        "josue", "maria", "moises",
        "noe", "salomao", "sansao",
        'abraao',"moises", "sansao",
    ]

    # Criando jogadores
    player7 = Players_in_Match(7, GAME_STANDARD_CARDS_SLUGS)
    player2 = Players_in_Match(2, GAME_STANDARD_CARDS_SLUGS.copy())
    player4 = Players_in_Match(4, GAME_STANDARD_CARDS_SLUGS.copy().copy())

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

    # # # Player7 change the deck
    # # player7 = Players_in_Match(7, [1, 2, 3, 4, 6, 5, 8, 2, 3, 1, 1, 1, 3])
    # # change_deck_player7 = GameData(data_type='change_deck', player=player7)
    # # game.gameHandle(change_deck_player7)

    # Player7 is ready
    ready_player7 = GameData(data_type='ready', player_id=player7.id)
    game.gameHandle(ready_player7)

    # # # Player2 is not ready
    # # ready_player2 = GameData(data_type='unready', player_id=player2.id)
    # # game.gameHandle(ready_player2)

    # Player4 is ready
    ready_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(ready_player4)


# STAGE 1
if __name__ == "__main__":

    # # Player7 1 retry all cards
    # retry_player7 = GameData(
    #     data_type='retry',
    #     player_id=player7.id,
    #     retry_cards=[
    #         *player7.card_hand[:]
    #     ]
    # )
    # game.gameHandle(retry_player7)

    # # Player7 2 retry first and last cards
    # retry_player7 = GameData(
    #     data_type='retry',
    #     player_id=player7.id,
    #     retry_cards=[
    #         player7.card_hand[0],
    #         player7.card_hand[-1]
    #     ]
    # )
    # game.gameHandle(retry_player7)

    # # Player7 3 retry the last cards
    # retry_player7 = GameData(
    #     data_type='retry',
    #     player_id=player7.id,
    #     retry_cards=[
    #         player7.card_hand[0],
    #     ]
    # )
    # game.gameHandle(retry_player7)

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

    # Player7 is ready
    ready_player7 = GameData(data_type='ready', player_id=player7.id)
    game.gameHandle(ready_player7)

    # Player2 is ready
    ready_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(ready_player2)

    # Player4 is ready
    ready_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(ready_player4)

# STAGE 2: THE GAME
# ROUND 1
if __name__ == "__main__":

    # Player4 moves first card to prepare zone
    move_4 = Move(player_move=player4.id,
                  card_id=player4.card_hand[1], move_type='move_to_prepare')
    move_player4 = GameData(
        data_type='move', player_id=player4.id, move=move_4)
    game.gameHandle(move_player4)

    # Player4 finishes their turn
    finish_player4 = GameData(data_type='ready', player_id=player4.id)
    game.gameHandle(finish_player4)

    # Player7 moves last card to prepare zone
    move_7 = Move(player_move=player7.id,
                  card_id=player7.card_hand[1], move_type='move_to_prepare')
    move_player7 = GameData(
        data_type='move', player_id=player7.id, move=move_7)
    game.gameHandle(move_player7)

    # Player7 finishes their turn
    finish_player7 = GameData(data_type='ready', player_id=player7.id)
    game.gameHandle(finish_player7)

    # Player2 moves last card to prepare zone
    move_2 = Move(player_move=player2.id,
                  card_id=player2.card_hand[1], move_type='move_to_prepare')
    move_player2 = GameData(
        data_type='move', player_id=player2.id, move=move_2)
    game.gameHandle(move_player2)

    # Player2 finishes their turn
    finish_player2 = GameData(data_type='ready', player_id=player2.id)
    game.gameHandle(finish_player2)

# ROUND 2
if __name__ == "0__main__":

    # Stage 0: Move to prepare

    # Player4 moves second card to prepare zone
    move_4 = Move(player_move=player4.id,
                  card_id=player4.card_hand[0], move_type='move_to_prepare')
    move_player4 = GameData(
        data_type='move', player_id=player4.id, move=move_4)
    game.gameHandle(move_player4)

    # # Stage 1: Move to battle

    # # Player4 moves first card from prepare zone to battle zone
    # move_4 = Move(player_move=player4.id,
    #               card_id=player4.card_prepare_camp[0], move_type='move_to_battle')
    # move_player4 = GameData(
    #     data_type='move', player_id=player4.id, move=move_4)
    # game.gameHandle(move_player4)
    
    # # Player4 finishes their turn
    # finish_player4 = GameData(data_type='ready', player_id=player4.id)
    # game.gameHandle(finish_player4)
