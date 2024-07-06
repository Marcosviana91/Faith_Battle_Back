from utils import DB, WS, GameRoom

from schemas import PlayersInMatchSchema, GameRoomSchema, GameData, APIResponseProps, ClientRequestProps


class RoomManager:
    ROOMS: list[GameRoomSchema]

    def __init__(self) -> None:
        self.ROOMS = []

    async def handleGamesRoom(self, data_raw):
        print(__file__, "\nRoomManager.handleGamesRoom")
        data = ClientRequestProps(**data_raw)
        print('>>>>> RECV: ', data.__dict__)
        response = APIResponseProps(message="")
        match data.data_type:
            case 'player_logged_in':
                response.message = f'Player {
                    data.user_data.get('id')} has logged in the game.'
                response.data_type = 'player_logged_in'
                response.user_data = {"id": data.user_data.get('id')}
                await WS.sendToPlayer(user_id=data.user_data.get('id'), player_state=response.__dict__)

            case 'create':
                player_db = DB.getPlayerById(data.room_data["created_by"])
                player = PlayersInMatchSchema(
                    id=player_db["id"], card_deck=player_db['available_cards'])
                new_room = GameRoom(
                    player,
                    data.room_data['room_name'],
                    data.room_data['room_max_players'],
                    data.room_data['room_game_type'],
                    data.room_data['password']
                )
                self.ROOMS.append(new_room)
                response.data_type = 'created'
                response.message = f'Player {
                    player.id} has created a room {new_room.id}'
                response.room_data = new_room.__dict__
                await WS.sendToPlayer(user_id=data.user_data.get('id'), player_state=response.__dict__)

            case 'connect':
                room = self.getRoomById(data.room_data.get('id'))
                player_db = DB.getPlayerById(data.user_data.get("id"))
                player = PlayersInMatchSchema(
                    id=player_db["id"], card_deck=player_db['available_cards'])
                data_handle = GameData(data_type=data.data_type, player=player)
                room.gameHandle(data_handle)

                response.message = f'Player {
                    player.id} has conected to room {room.id}'
                response.room_data = room.__dict__
                WS.enterRoom(player.id, room.id)
                await WS.sendToRoom(room_state=response.__dict__, room_id=room.id)

            case 'disconnect':
                room = self.getRoomById(data.room_data.get('id'))
                player_id = data.user_data.get('id')
                data_handle = GameData(
                    data_type=data.data_type, room_id=room.id, player_id=player_id)
                room.gameHandle(data_handle)
                if (room.players_in_match.__len__() < 1):
                    self.ROOMS.remove(room)
                response.message = f'Player {
                    player_id} has disconected from room {room.id}'
                response.data_type = 'disconnected'
                response.room_data = room.__dict__
                WS.leaveRoom(player_id, room.id)
                await WS.sendToRoom(room_state=response.__dict__, room_id=room.id)
                await WS.sendToPlayer(player_state=response.__dict__, user_id=player_id)

            case 'ready':
                room = self.getRoomById(data.room_data.get('id'))
                player_id = data.user_data.get('id')
                data_handle = GameData(data_type='ready', player_id=player_id)

                game_response = room.gameHandle(data_handle)
                if (game_response == 'ready'):
                    player_state = {
                        "data_type": "player_update",
                        "player_data": {
                            "id": player_id,
                            "ready": True,
                            "cards_in_hand": self.getPlayerInRoomById(room=room, player_id=player_id).card_hand
                        }
                    }
                    await WS.sendToPlayer(player_state=player_state, user_id=player_id)

                elif (game_response == 'starting_stage_1'):
                    print('Enviar as cartas da mão para cada jogador da sala:')
                    for player in room.players_in_match:
                        player_state = {
                            "data_type": "player_update",
                            "player_data": {
                                "id": player.id,
                                "ready": player.ready,
                                "cards_in_hand": player.card_hand
                            }
                        }
                        await WS.sendToPlayer(
                            player_state=player_state, user_id=player.id)
                        player.id
                elif (game_response == 'starting_stage_2'):
                    print('Enviar as cartas da mão para cada jogador da sala:')
                    # for player in room.players_in_match:
                    #     player_state = {
                    #         "data_type": "player_update",
                    #         "player_data": {
                    #             "id": player.id,
                    #             "cards_in_hand": player.card_hand
                    #         }
                    #     }
                    #     await WS.sendToPlayer(
                    #         player_state=player_state, user_id=player.id)
                    #     player.id

                response.message = f'Player {player_id} is ready.'
                response.data_type = 'room_update'
                response.room_data = room.__dict__
                await WS.sendToRoom(room_state=response.__dict__, room_id=room.id)

    def getRoomById(self, room_id):
        for room in self.ROOMS:
            if room.id == room_id:
                return room

    def getPlayerInRoomById(self, room: GameRoomSchema, player_id):
        for player in room.players_in_match:
            if player.id == player_id:
                return player

    def getRoomInfoById(self, room_id):
        room_id = int(room_id)
        room = self.getRoomById(room_id)
        if room:
            room_info = {
                "room_name": room.room_name,
                "created_by": room.created_by,
                "players_in_match": room.getPlayersIdList(),
                "max_players": room.max_players,
                "match_type": room.match_type,
                "password": room.password,
                "game_stage": room.game_stage,
                "round": room.round,
                "player_turn": room.player_turn,

            }
            return room_info
        return {"messsage": "Room not found"}

    def getPlayerInRoomInfoById(self, room_id, player_id):
        room_id = int(room_id)
        player_id = int(player_id)

        room = self.getRoomById(room_id)
        if room:
            for player in room.players_in_match:
                if player.id == player_id:
                    player_info = {
                        "ready": player.ready,
                        "faith_points": player.faith_points,
                        "wisdom_points": player.wisdom_points,
                        "wisdom_used": player.wisdom_used,
                        "card_deck": player.card_deck,
                        "card_hand": player.card_hand,
                        "card_in_forgotten_sea": player.card_in_forgotten_sea,
                        "card_prepare_camp": player.card_prepare_camp,
                        "card_battle_camp": player.card_battle_camp,

                    }
                    return player_info
        return {"messsage": "Room or Player not found"}

    def getAllRoomsInfo(self):
        response = APIResponseProps(message="0 room founded")
        for room in self.ROOMS:
            response.room_list.append(room.__dict__)
        if response.room_list.__len__() > 0:
            response.data_type = "room_list"
            response.message = f"{response.room_list.__len__()} room founded"
        return response

    def endRoom(self, room):
        self.ROOMS.remove(room)
        del room


ROOMS = RoomManager()
