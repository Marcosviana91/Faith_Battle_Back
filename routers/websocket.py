# from typing import Annotated

from fastapi import APIRouter,  WebSocket, WebSocketDisconnect

from schemas.users_schema import UserWs
from utils.CheckUserState import checkUserStats
from utils.ConnectionManager import WS, WSFlat
from utils.ROOM.RoomManager import RM
from utils.MATCHES.MatchManager import MM, C_Match

router = APIRouter(prefix="/ws", tags=["websockets"])

# Rota para o jogo gerenciado pela API
@router.websocket("/")
async def handleWSConnect(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()
            if data.get("data_type") == "create_connection":
                player_id = int(data["player_data"]["id"])
                player_token = data["player_data"]["token"]
                newUserWs = UserWs(
                    id=player_id,
                    access_token=player_token,
                    websocket=websocket
                )
                await WS.connect(newUserWs)
                await checkUserStats(player_id)
            elif data.get("data_type") == "match_move":
                await MM.handleMove(data)
            else:
                room = await RM.handleRoom(data)
                if room.room_stage == 2:
                    newMatch = C_Match(room=room)
                    await RM.endRoom(room)
                    await MM.createMatch(newMatch)

    except WebSocketDisconnect:
        WS.disconnect(player_id)


@router.websocket("/flat")
async def handleWSFlatConnect(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()
            print('RECV <<<:', data)
            if data.get('data_type') == "create_connection":
                name = data['player_data']['name']
                sala = data['player_data']['sala']
                await WSFlat.connect(name, sala, websocket)
            elif data.get('data_type') == "give_card":
                await WSFlat.giveCards(sala=sala, name=name)
            else:
                await WSFlat.send2Room(room=sala, data=data)

    except WebSocketDisconnect:
        pass
        # WSFlat.disconnect(name, sala)


@router.websocket("/spectate/{match_id}")
async def enterRoom(websocket: WebSocket, match_id: str, password: str = ""):
    await websocket.accept()
    try:
        while True:
            data: dict = await websocket.receive_json()

    except WebSocketDisconnect:
        ...


@router.get("/")
async def handleMatchWS():
    return WS.getStats()
