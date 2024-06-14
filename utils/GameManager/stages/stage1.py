# Stage 1: Sort cards to all players, retry sort
from models.schemas import GameData, GameRoomSchema, Players_in_Match


MAXIMUM_DECK_TRIES = 3

def retryCard(self: GameRoomSchema, player: Players_in_Match, cards: list):
    # print(f'Retring {cards.__len__()} cards to player {player.id}')
    # print(player.deck_try)
    if player.deck_try < MAXIMUM_DECK_TRIES:
        for card in cards:
            player.card_hand.remove(card)
            player.card_deck.append(card)
        self.giveCard(player, cards.__len__())
        player.deck_try += 1
        if player.deck_try >= MAXIMUM_DECK_TRIES:
            ready_player = GameData(data_type='ready', player_id=player.id)
            dataHandle(self, ready_player)
    else:
        raise BaseException(f'Player {player.id} reaches maximum retries')


def dataHandle(self: GameRoomSchema, data: GameData):
    match data.data_type:
        case  "retry":
            print('Retry')
            player = self.getPlayerByPlayerId(data.player_id)
            retryCard(self, player, data.retry_cards)

        case "ready":
            player = self.getPlayerByPlayerId(data.player_id)
            player.ready = True
            print(f"Player {data.player_id} is ready.")
            self.allPlayersIsReady()

        case "unready":
            player = self.getPlayerByPlayerId(data.player_id)
            if player.deck_try < MAXIMUM_DECK_TRIES:
                player.ready = False
                print(f"Player {data.player_id} is not ready.")
            else:
                print(f"Player {data.player_id} cannot be not ready.")
