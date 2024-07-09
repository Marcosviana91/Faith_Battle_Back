# from typing import Annotated

from fastapi import APIRouter, Depends, WebSocketDisconnect, status, WebSocket

from utils.RoomManager import ROOMS
from utils.MatchManager import MATCHES
from utils.ConnectionManager import WS
from schemas import UserWs

# from utils.security import getCurrentUserAuthenticated

router = APIRouter(prefix="/ws", tags=["websockets"])

# T_CurrentUser = Annotated[str, Depends(getCurrentUserAuthenticated)]


@router.websocket("/")
async def handleWSConnect(websocket: WebSocket):
    await websocket.accept()
    player_id = None
    try:
        while True:
            data: dict = await websocket.receive_json()
            if data.get("data_type") == "create_connection":
                player_id = data["player_data"]["id"]
                player_token = data["player_data"]["token"]
                newUserWs = UserWs(
                    id=player_id,
                    token=player_token,
                    websocket=websocket
                )
                WS.connect(newUserWs)
            else:
                await ROOMS.handleRoom(data)

    except WebSocketDisconnect:
        WS.disconnect(player_id)

@router.get("/")
async def handleMatchWS():
    return MATCHES.getStats()