# Stage 2: The game is in curse
import asyncio


from models.schemas import GameData, GameRoomSchema, Players_in_Match


# MAXIMUM_DECK_TRIES = 3


def dataHandle(self: GameRoomSchema, data: GameData):
    match data.data_type:
        case  "move":
            print('Moving')
            player = self.getPlayerByPlayerId(data.player_id)


        case "ready":
            player = self.getPlayerByPlayerId(data.player_id)
            player.ready = True
            print(f"Player {data.player_id} is ready.")
            self.allPlayersIsReady()

