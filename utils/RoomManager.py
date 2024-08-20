from schemas.API_schemas import ClientRequestSchema
from schemas.matches_schema import MatchSchema
from schemas.players_schema import PlayersSchema
from schemas.rooms_schema import RoomSchema
from utils.Cards import cardListToDict
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.MatchManager import MATCHES

from utils.console import consolePrint
from utils.LoggerManager import Logger


class RoomManager:
    ROOMS: list[RoomSchema]

    def __init__(self) -> None:
        self.ROOMS = []

    def _getRoomById(self, room_id: str) -> RoomSchema:
        for room in self.ROOMS:
            if room.id == room_id:
                return room
        consolePrint.danger(f'Room ID not found: {room_id}')
        return None

    def getAllRoomsInfo(self):
        if len(self.ROOMS) < 1:
            return False
        response = []
        for room in self.ROOMS:
            response.append(room.getRoomStats)
        return response

    def getRoomInfo(self, room_id):
        room = self._getRoomById(room_id)
        return room.getRoomStats

    def createRoom(self, room: RoomSchema):
        self.ROOMS.append(room)
        DB.setPlayerInRoom(
            player_id=room.connected_players[0].id, room_id=room.id)
        Logger.info(f'Room {room.id} created', 'ROOMS')
        return room.getRoomStats

    def endRoom(self, room:RoomSchema):
        self.ROOMS.remove(room)
        consolePrint.info(f'Room {room.id} finished')
        Logger.info(f'Room {room.id} finished', 'ROOMS')
        del room

    async def enterRoom(self, room_id: str, player: PlayersSchema, password: str):
        room = self._getRoomById(room_id)
        room_stats = room.connect(player, password)
        DB.setPlayerInRoom(player_id=player.id, room_id=room_id)
        for player in room.connected_players:
            await WS.sendToPlayer({"data_type": "room_update", "room_data": room_stats}, player.id)
        return room_stats

    async def handleRoom(self, data_raw):
        Logger.info(f'>>>: {data_raw}', 'ROOMS')
        data = ClientRequestSchema(**data_raw)
        consolePrint.status(f'>>>>> RECV: {data}')
        match data.data_type:
            case 'disconnect':
                room = self._getRoomById(data.room_data.get('id'))
                player_id = data.user_data.get('id')
                room.disconnect(player_id)
                DB.setPlayerInRoom(
                    player_id=player_id, room_id="")
                await WS.sendToPlayer({"data_type": "disconnected"}, player_id)
                if len(room.connected_players) == 0:
                    self.endRoom(room)
                else:
                    for player in room.connected_players:
                        await WS.sendToPlayer({"data_type": "room_update", "room_data": room.getRoomStats}, player.id)
            case 'ready':  # Aplicar DRY com 'retry_cards'
                room = self._getRoomById(data.room_data.get('id'))
                player_id = data.user_data.get('id')
                room.setReady(player_id)
                if room.room_stage == 1:
                    for player in room.connected_players:
                        await WS.sendToPlayer(
                            {
                                "data_type": "player_update",
                                "player_data": {
                                    "id": player.id,
                                    "deck_try": player.deck_try,
                                    "ready": player.ready,
                                    "card_hand": cardListToDict(player.card_hand)
                                }
                            },
                            player.id
                        )
                for player in room.connected_players:
                    await WS.sendToPlayer(
                        {
                            "data_type": "room_update",
                            "room_data": room.getRoomStats
                        }, player.id
                    )
                if room.room_stage == 2:
                    newMatch = MatchSchema(room=room)
                    await MATCHES.createMatch(newMatch)
                    await newMatch.updatePlayers()
                    # for player in room.connected_players:
                    #     await WS.sendToPlayer(
                    #         {
                    #             "data_type": "match_update",
                    #             "match_data": newMatch.getMatchStats
                    #         },
                    #         player.id
                    #     )
                    self.endRoom(room)
            case 'retry_cards':  # Aplicar DRY com 'ready'
                room = self._getRoomById(data.room_data.get('id'))
                player_id = data.user_data.get('id')
                cards_list = data.retry_cards
                player = room.retryCard(player_id, cards_list)
                if (player.ready):
                    for _player in room.connected_players:
                        await WS.sendToPlayer(
                            {
                                "data_type": "room_update",
                                "room_data": room.getRoomStats
                            }, _player.id
                        )
                await WS.sendToPlayer(
                    data={
                        "data_type": "player_update",
                        "player_data": {
                            "id": player_id,
                            "ready": player.ready,
                            "deck_try": player.deck_try,
                            "card_hand": cardListToDict(player.card_hand)
                        }
                    },
                    user_id=player_id
                )
                if room.room_stage == 2:
                    newMatch = MatchSchema(room=room)
                    await MATCHES.createMatch(newMatch)
                    await newMatch.updatePlayers()
                    self.endRoom(room)


ROOMS = RoomManager()
