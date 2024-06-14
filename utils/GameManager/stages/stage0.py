# Stage 0: players has connecteds, check decks
from collections import defaultdict

from models.schemas import GameData, GameRoomSchema


MINIMUM_DECK_CARDS = 10
MAXIMUM_CARDS_REPEATS = 2

def checkDeckCardsRepeats(deck: list) -> list:
    result = []
    keys = defaultdict(list)
    for key, value in enumerate(deck):
        keys[value].append(key)

    for value in keys:
        if len(keys[value]) > MAXIMUM_CARDS_REPEATS:
            result.append(value)
    return result

def dataHandle(self: GameRoomSchema, data: GameData):
    match data.data_type:
        case  "connect":
            self.players_in_match.append(data.player)
            print(f"Player {data.player.id} connected.")
        case  "disconnect":
                    self.players_in_match.remove(data.player)
                    print(f"Player {data.player.id} disconnected.")
        case "ready":
            player = self.getPlayerByPlayerId(data.player_id)
            # Checando se o deck está ok
            checkDeckCards_result = checkDeckCardsRepeats(player.card_deck)
            if checkDeckCards_result.__len__() > 0:
                print(f"Player {data.player_id} is not ready due cards {checkDeckCards_result} exceed maximum repeats")
            elif player.card_deck.__len__() < MINIMUM_DECK_CARDS:
                print(f"Player {data.player_id} is not ready due their deck has less than 30 cards")
            else:
                player.ready = True
                print(f"Player {data.player_id} is ready.")
            if self.allPlayersIsReady():
                for player in self.players_in_match:
                    self.giveCard(player,5)
        case "unready":
            player = self.getPlayerByPlayerId(data.player_id)
            player.ready = False
            print(f"Player {data.player_id} is not ready.")
        case "change_deck":
            player = self.getPlayerByPlayerId(data.player.id)
            player.card_deck = data.player.card_deck
            print(f"Player {data.player.id} has change their deck.")