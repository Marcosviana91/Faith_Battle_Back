from fastapi import WebSocket


class RoomWS:
    def __init__(self, id: int):
        self.id = id
        self.players: list[UserWS] = []


class UserWS:
    def __init__(self, id: int, ws: WebSocket):
        self.id = id
        self.ws = ws


class WS_Manager:
    def __init__(self):
        self.all_users: list[UserWS] = []
        self.all_rooms: list[RoomWS] = []
        
    
    def __getRoom(self, room_id: int) -> RoomWS:
        for room in self.all_rooms:
            if room.id == room_id:
                return room
        print(__file__, f"\nWS: Room {room_id} not found.\nCreating...")
        new_room = RoomWS(id=room_id)
        self.all_rooms.append(new_room)
        return new_room
    
    def __getUser(self, user_id: int) -> UserWS:
        for user in self.all_users:
            if user.id == user_id:
                return user

    def connect(self, websocket: WebSocket, user_id: int = None):
        new_user_ws_conn = UserWS(id=user_id, ws=websocket)
        self.all_users.append(new_user_ws_conn)
        print(__file__, f"\nWS: User {user_id} has connected.")
        print(__file__, f"\nWS: Users connected in game: {self.all_users.__len__()}.")

    def disconnect(self, user_id: int = None):
        user = self.__getUser(user_id)
        self.all_users.remove(user)
        print(__file__, f"\nWS: User {user_id} has disconnected.")
        print(__file__, f"\nWS: Users connected in game: {self.all_users.__len__()}.")
                
    def enterRoom(self, user_id:int, room_id:int):
        room = self.__getRoom(room_id)
        user = self.__getUser(user_id)
        room.players.append(user)
        print(__file__, f"\nWS: User {user_id} enter in room {room_id}.")
        print(__file__, f"\nWS: Users connected {room.players.__len__()}.")

    def leaveRoom(self, user_id:int, room_id:int):
        room = self.__getRoom(room_id)
        user = self.__getUser(user_id)
        room.players.remove(user)
        if room.players.__len__() < 1:
            self.all_rooms.remove(room)
        print(__file__, f"\nWS: User {user_id} has leave the room {room_id}.")
        print(__file__, f"\nWS: Users connected {room.players.__len__()}.")

    async def sendToPlayer(self, player_state: dict, user_id:int):
        user = self.__getUser(user_id)
        print(f"WS: Send to player {user_id}: {player_state}")
        await user.ws.send_json(player_state)

    async def sendToRoom(self, room_state: dict, room_id: int):
        # Remover dados sensíveis
        __room_state = dict(room_state)
        __room_state["data_type"] = "room_update"
        __room_state.pop("user_data", "")
        __room_state.pop("room_list", "")
        __room_state.pop("player_data", "")
        __room_state['data_type'] = 'room_update'
        print("sendToRoom: ", __room_state)
        
        print(f"WS: Broadcast to room {room_id}.")
        room = self.__getRoom(room_id)
        print(f"WS:\tPlayers in room: {room.players.__len__()}.")
        for user in room.players:
            await user.ws.send_json(__room_state)
            
    async def sendToAll(self, message):
        for user in self.all_users:
            await user.ws.send_json(message)

WS = WS_Manager()