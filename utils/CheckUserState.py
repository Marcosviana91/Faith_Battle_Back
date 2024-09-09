# Check if User is in room or match and send to user the actual state
from utils.ROOM.RoomClass import cardListToDict
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.MATCHES.MatchManager import MM
from utils.ROOM.RoomManager import RM


async def checkUserStats(player_id: int):
    room_id = dict(await DB.getPlayerById(player_id)).get("room_id", None)
    match_id = dict(await DB.getPlayerById(player_id)).get("match_id", None)
    # Enviar um leave room para o cliente caso não exista a sala nem partida
    if room_id is None and match_id is None:
        # await DB.setPlayerRoomOrMatch(player_id)
        # await WS.sendToPlayer({"data_type": "disconnected"}, player_id)
        return None

    room = RM._getRoomById(room_id)
    if room:
        for team in room.connected_players:
            for player in team:
                if player.id == player_id:
                    room_to_send = {
                        "data_type": "room_update",
                        "room_data": room.getStats()
                    }
                    player_to_send = {
                        "data_type": "player_update",
                        "player_data": {
                            "id": player.id,
                            "ready": player.ready,
                            "deck_try": player.deck_try,
                            "card_hand": cardListToDict(player.card_hand),
                        }
                    }
                    await WS.sendToPlayer(data=player_to_send, user_id=player_id)
                    await WS.sendToPlayer(data=room_to_send, user_id=player_id)

    else:
        match = MM._getMatchById(match_id)
        if match:
            for _team in match.players_in_match:
                for player in _team:
                    if player.id == player_id:
                        match_to_send = {
                            "data_type": "match_update",
                            "match_data": match.getStats()
                        }
                        player_to_send = {
                        "data_type": "player_update",
                        "player_data": player.getStats(private=True)
                    }
                        await WS.sendToPlayer(data=player_to_send, user_id=player_id)
                        await WS.sendToPlayer(data=match_to_send, user_id=player_id)
                        for _card in player.card_prepare_camp:
                            if _card.card_type == "miracle":
                                await WS.sendToPlayer(
                                    data={
                                        "data_type": "card_skill",
                                        "card_data": {
                                            "slug": _card.slug,
                                        }
                                    },
                                    user_id=player.id
                                )
    return None
