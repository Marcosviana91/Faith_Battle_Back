from schemas.API_schemas import ClientRequestSchema
from schemas import PlayersSchema
from utils.ROOM.RoomClass import C_Room
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.MATCHES.MatchManager import MM

from utils.console import consolePrint
# from utils.LoggerManager import Logger

from schemas import RoomSchema


class RoomManager:
    ROOMS: list[C_Room]

    def __init__(self) -> None:
        self.ROOMS = []

    async def createRoom(self, room: RoomSchema):
        new_room = C_Room(**room.model_dump())
        await new_room.connect()
        self.ROOMS.append(new_room)
        # DB.setPlayerInRoom(
        #     player_id=room.connected_players[0].id, room_id=room.id)
        # Logger.info(f'Room {room.id} created', 'ROOMS')
        return new_room.getStats()

    def getAllRoomsStats(self):
        if len(self.ROOMS) < 1:
            return False
        response = []
        for room in self.ROOMS:
            response.append(room.getStats())
        return response

    def _getRoomById(self, room_id: str) -> C_Room:
        for room in self.ROOMS:
            if room.id == room_id:
                return room
        consolePrint.danger(f'Room ID not found: {room_id}')
        return None

#     def getRoomInfo(self, room_id):
#         room = self._getRoomById(room_id)
#         return room.getRoomStats

    async def endRoom(self, room: C_Room):
        self.ROOMS.remove(room)
        consolePrint.info(f'Room {room.id} finished')
        # Logger.info(f'Room {room.id} finished', 'ROOMS')
        for _team in room.connected_players:
            for player in _team:
                await DB.setPlayerRoomOrMatch(player_id=player.id, clear=True)
        del room

    async def enterRoom(self, room_id: str, player: PlayersSchema, password: str):
        room = self._getRoomById(room_id)
        room_stats = await room.connect(player.id, password)
        for _player in room.connected_players[0]:
            await WS.sendToPlayer({"data_type": "room_update", "room_data": room_stats}, _player.id)
        return room_stats

    async def handleRoom(self, data_raw):
        # Logger.info(f'>>>: {data_raw}', 'ROOMS')
        data = ClientRequestSchema(**data_raw)
        consolePrint.status(f'>>>>> RECV: {data}')
        room = self._getRoomById(data.room_data.get('id'))
        player_id = data.user_data.get('id')
        match data.data_type:
            case 'disconnect':
                print(f"Desconectar p:{player_id} da sala {room.id}")
                await room.disconnect(player_id)
                await WS.sendToPlayer({"data_type": "disconnected"}, player_id)
                if len(room.connected_players) == 0:
                    await self.endRoom(room)
                else:
                    for player in room.connected_players[0]:
                        await WS.sendToPlayer({"data_type": "room_update", "room_data": room.getStats()}, player.id)

            case 'ready':  # Aplicar DRY com 'retry_cards'
                room.setReady(player_id)
                if room.room_stage == 1:
                    for team in room.connected_players:
                        for player in team:
                            await WS.sendToPlayer(
                                {
                                    "data_type": "player_update",
                                    "player_data": player.getStats()
                                },
                                player.id
                            )
                for team in room.connected_players:
                    for player in team:
                        await WS.sendToPlayer(
                            {
                                "data_type": "room_update",
                                "room_data": room.getStats()
                            }, player.id
                        )

            case 'retry_cards':  # Aplicar DRY com 'ready'
                cards_list = data.retry_cards
                player = room.retryCard(player_id, cards_list)
                if (player.ready):
                    for team in room.connected_players:
                        for _player in team:
                            await WS.sendToPlayer(
                                {
                                    "data_type": "room_update",
                                    "room_data": room.getStats()
                                }, _player.id
                            )
                await WS.sendToPlayer(
                    data={
                        "data_type": "player_update",
                        "player_data": player.getStats()
                    },
                    user_id=player_id
                )

        return room


RM = RoomManager()
