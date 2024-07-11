# Check if User is in room or match and send to user the actual state
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.RoomManager import ROOMS


async def checkUserStats(player_id):
    room_id = DB.getPlayerById(player_id).get("room_or_match_id")
    if room_id is None:
        return None
    room = ROOMS._getRoomById(room_id)
    for player in room.connected_players:
        if player.id == player_id:
            room_to_send = {
                "data_type": "room_update",
                "room_data": room.getRoomStats
            }
            player_to_send = {
                "data_type": "player_update",
                "player_data": {
                    "id": player.id,
                    "ready": player.ready,
                    "cards_in_hand": player.card_hand
                }
            }
            await WS.sendToPlayer(data=room_to_send, user_id=player_id)
            await WS.sendToPlayer(data=player_to_send, user_id=player_id)
