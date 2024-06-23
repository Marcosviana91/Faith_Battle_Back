from fastapi import FastAPI, status, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from secrets import token_hex

from utils import WS, DB, ROOMS

# from utils.populates import UserPopulate

import json


ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()

secret_key = token_hex()

app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)


# @app.get('/match')
# def handleRoot(req: Request):
#     # crfs_token = token_hex(8)
#     # print("headers: ", req.headers)
#     # print("cookies: ", req.cookies)
#     # print("session: ", req.session)
#     # print("method: ", req.method)
#     # print("path_params: ", req.path_params)
#     # print("query_params: ", req.query_params)
#     rooms = ROOMS.getAllRoomsInfo()
#     res = JSONResponse(content=rooms)
#     # res.set_cookie("crfs_token", crfs_token)
#     # res.delete_cookie("crfs")
#     return res


@app.post('/auth')
async def handleAuth(req: Request):
    data = json.loads(await req.body())
    print("session: ", req.session)
    user_data = DB.authUser(
        username=data["username"],
        password=data["password"]
    )
    if user_data.data_type == 'error':
        res = JSONResponse(content=user_data.__dict__,
                           status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
    else:
        req.session['user_info'] = user_data.user_data
        res = JSONResponse(content=user_data.__dict__,
                           status_code=status.HTTP_202_ACCEPTED)
    return res


@app.post('/newuser')
async def handleNewUser(req: Request):
    data = json.loads(await req.body())
    user_data = DB.createNewUser(data)
    res = JSONResponse(content=user_data, status_code=status.HTTP_201_CREATED)
    return res


# Usado pelo cliente para obter uma lista de todas as salas que estão aguardando jogadores
@app.get('/match')
def handleMatchList(req: Request):
    rooms = ROOMS.getAllRoomsInfo()
    response = JSONResponse(content=rooms.__dict__)
    return response


@app.get('/match/{room_id}')
def handleMatchById(req: Request, room_id: str):
    print(room_id)
    room_info = ROOMS.getRoomInfoById(room_id)
    res = JSONResponse(content=room_info)
    return res


@app.get('/match/{room_id}/{player_id}')
def handlePlayerInMatch(req: Request, room_id: str, player_id: str):
    room_info = ROOMS.getPlayerInRoomInfoById(room_id, player_id)
    res = JSONResponse(content=room_info)
    return res


@app.websocket('/websocket_conn')
async def handleWebSockets(websocket: WebSocket):
    await websocket.accept()
    try:
        user_id = websocket.session.get("user_info").get("id")
    except AttributeError:
        user_id = 1

    WS.connect(websocket, user_id)
    try:
        while True:
            data:dict = await websocket.receive_json()
            __user_data = data.get('user_data', {"id": user_id})
            data['user_data'] = __user_data
            await ROOMS.handleGamesRoom(data)

    except WebSocketDisconnect:
        WS.disconnect(user_id)

    return None
