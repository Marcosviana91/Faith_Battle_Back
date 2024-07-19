# Check if User is in room or match and send to user the actual state
from utils.Cards import cardListToDict
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.RoomManager import ROOMS
from utils.MatchManager import MATCHES


async def checkUserStats(player_id):
    room_id = DB.getPlayerById(player_id).get("room_or_match_id")
    if not room_id:
        return None
    
    room = ROOMS._getRoomById(room_id)
    if room:
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
                        "card_hand": cardListToDict(player.card_hand),
                    }
                }
                await WS.sendToPlayer(data=player_to_send, user_id=player_id)
                await WS.sendToPlayer(data=room_to_send, user_id=player_id)
    else:
        match = MATCHES._getMatchById(match_id=room_id)
        if match:
            for player in match.players_in_match:
                if player.id == player_id:
                    match_to_send = {
                        "data_type": "match_update",
                        "match_data": match.getMatchStats
                    }
                    player_to_send = {
                        "data_type": "player_update",
                        "player_data": {
                            "id": player.id,
                            "card_hand": cardListToDict(player.card_hand),
                            "wisdom_points": player.wisdom_points,
                            "wisdom_available": player.wisdom_available
                        }
                    }
                    await WS.sendToPlayer(data=player_to_send, user_id=player_id)
                    await WS.sendToPlayer(data=match_to_send, user_id=player_id)
    return None