from utils import DB_Manager, GameRoom

from models.schemas import Players_in_Match, GameRoomSchema, GameData

DB = DB_Manager()


class RoomManager:
    ROOMS: list[GameRoomSchema]
    
    def __init__(self) -> None:
        self.ROOMS = []

    def newRoom(self, room_data):
        player_db = DB.getPlayerById(room_data["created_by"])
        player = Players_in_Match(
            id=player_db["id"], card_deck=player_db['available_cards'])
        new_room = GameRoom(
            player,
            room_data['room_name'],
            room_data['max_players'],
            room_data['match_type'],
            room_data['password']
        )
        self.ROOMS.append(new_room)
        print(__file__,'\n',self.ROOMS[-1].players_in_match)
        return new_room.id
    
    def handleGamesRoom(self, room_id, user_id, data):
        # print(data, room_id, user_id)
        room = self.getRoomById(room_id)
        player_db = DB.getPlayerById(user_id)
        player = Players_in_Match(id=player_db["id"], card_deck=player_db['available_cards'])
        match data['data_type']:
            case 'connect':
                con_player = GameData(data_type=data['data_type'], player=player)
                room.gameHandle(con_player)
        print(__file__,'\n',self.ROOMS[-1].players_in_match)

    def getRoomById(self, room_id):
        pass
        for room in self.ROOMS:
            if room.id == room_id:
                return room

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
        __temp_array = []
        for room in self.ROOMS:
            room_info = {
                "id": room.id,
                "created_by": room.created_by,
                "room_name": room.room_name,
                "room_game_type": 'survival',
                "room_current_players": room.players_in_match.__len__(),
                "room_max_players": room.max_players,
                "has_password": (room.password != ""),
            }
            __temp_array.append(room_info)
        return __temp_array

    def endRoom(self, room):
        self.ROOMS.remove(room)
        del room
