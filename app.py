# from utils.GameManager import GameRoom
# , GameSchema, MoveSchema, CardSchema
from schemas.games_schema import RoomSchema
from schemas.players_schema import PlayersSchema
from pprint import pprint

# from utils.populates.CardPopulate import cardPopulates

# STAGE 0
if __name__ == "__main__":
    GAME_STANDARD_CARDS_SLUGS = [
        'abraao', 'adao', 'daniel',
        'davi', 'elias', 'ester',
        'eva', 'jaco', "jose-do-egito",
        "josue", "maria", "moises",
        "noe", "salomao", "sansao",
    ]

    # Criando jogadores
    player7 = PlayersSchema(
        id=7, available_cards=GAME_STANDARD_CARDS_SLUGS
    )
    player2 = PlayersSchema(
        id=2, available_cards=GAME_STANDARD_CARDS_SLUGS.copy())
    player4 = PlayersSchema(
        id=4, available_cards=GAME_STANDARD_CARDS_SLUGS.copy().copy())

    # Player4 cria a sala do jogo
    game_room_4 = RoomSchema(
        created_by=player4, name="Sala do J4", max_players=3, password='123abc')

    # Connecting player7
    game_room_4.connect(player7, '123abc')

    # Connecting player2
    game_room_4.connect(player2, '123abc')

    # Player2 is ready
    game_room_4.setReady(player2.id)

    # Player7 change the deck
    game_room_4.setDeck(player7.id, [
        'abraao', 'adao', 'daniel',
        'davi', 'elias', 'ester',
        'eva', 'jaco', "jose-do-egito",
        "josue", "maria", "moises",
        "noe", "salomao", "sansao",
        'abraao', "moises", "sansao",
    ])

    # Player7 is ready
    game_room_4.setReady(player7.id)

    # Player4 is ready
    game_room_4.setReady(player4.id)


# STAGE 1
if __name__ == "__main__":

    # Player7 1 retry all cards
    game_room_4.retryCard(
        player7.id,
        cards=[*player7.card_hand[:]]
    )

    # Player7 2 retry first and last cards
    game_room_4.retryCard(
        player7.id,
        cards=[player7.card_hand[0], player7.card_hand[-1]]
    )

    # Player7 3 retry the last cards
    game_room_4.retryCard(
        player7.id,
        cards=[player7.card_hand[0]]
    )

    # # Player7 4 retry the last cards / Not allowed: raise Exception
    # game_room_4.retryCard(
    #     player7.id,
    #     cards=[player7.card_hand[0]]
    # )

    # # Player7 is not ready
    # game_room_4.setNotReady(player7.id)

#     # Player4 is ready
    game_room_4.setReady(player4.id)
    
#     # Player2 is ready
    game_room_4.setReady(player2.id)


# STAGE 2: THE GAME
# ROUND 1
if __name__ == "__main__":
    game_match_4 = game_room_4.getMatch()
    pprint(game_match_4.getMatchStats)

    # Player4 moves first card to prepare zone
    game_match_4.moveCard(player_id=player4.id, )

#     # Player4 finishes their turn
#     finish_player4 = GameSchema(data_type='ready', player_id=player4.id)
#     game.gameHandle(finish_player4)

#     # Player7 moves last card to prepare zone
#     move_7 = MoveSchema(player_move=player7.id,
#                   card_id=player7.card_hand[1], move_type='move_to_prepare')
#     move_player7 = GameSchema(
#         data_type='move', player_id=player7.id, move=move_7)
#     game.gameHandle(move_player7)

#     # Player7 finishes their turn
#     finish_player7 = GameSchema(data_type='ready', player_id=player7.id)
#     game.gameHandle(finish_player7)

#     # Player2 moves last card to prepare zone
#     move_2 = MoveSchema(player_move=player2.id,
#                   card_id=player2.card_hand[1], move_type='move_to_prepare')
#     move_player2 = GameSchema(
#         data_type='move', player_id=player2.id, move=move_2)
#     game.gameHandle(move_player2)

#     # Player2 finishes their turn
#     finish_player2 = GameSchema(data_type='ready', player_id=player2.id)
#     game.gameHandle(finish_player2)

# ROUND 2
if __name__ == "0__main__":

#     # Stage 0: Move to prepare

#     # Player4 moves second card to prepare zone
#     move_4 = MoveSchema(player_move=player4.id,
#                   card_id=player4.card_hand[0], move_type='move_to_prepare')
#     move_player4 = GameSchema(
#         data_type='move', player_id=player4.id, move=move_4)
#     game.gameHandle(move_player4)

#     # # Stage 1: Move to battle

#     # # Player4 moves first card from prepare zone to battle zone
#     # move_4 = MoveSchema(player_move=player4.id,
#     #               card_id=player4.card_prepare_camp[0], move_type='move_to_battle')
#     # move_player4 = GameSchema(
#     #     data_type='move', player_id=player4.id, move=move_4)
#     # game.gameHandle(move_player4)

#     # # Player4 finishes their turn
#     # finish_player4 = GameSchema(data_type='ready', player_id=player4.id)
#     # game.gameHandle(finish_player4)
