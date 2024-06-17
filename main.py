from fastapi import FastAPI, status
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from secrets import token_hex

from utils import WS_Manager, DB_Manager, RoomManager

from utils.populates import UserPopulate

import json

from pydantic import BaseModel


class Data(BaseModel):
    data: dict


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
DB = DB_Manager()
ROOMS = RoomManager.RoomManager()


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


@app.get('/match')
def handleMatchList(req: Request):
    rooms = ROOMS.getAllRoomsInfo()
    res = JSONResponse(content=rooms)
    return res


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


@app.post("/match")
async def handleCreateMatch(req: Request):
    data = json.loads(await req.body())['data']
    room_id = ROOMS.newRoom(data)
    res = JSONResponse(content=room_id)
    return res


@app.post("/match/handle/{room_id}")
async def handleGamesRoom(req: Request, room_id: int):
    try:
        user_id = req.session['user_info']['id']
    except KeyError:
        user_id = 1
    
    data = json.loads(await req.body())
    ROOMS.handleGamesRoom(room_id, user_id, data)
    # res = JSONResponse(content=room_id)
    # return res


@app.post('/auth')
async def handleAuth(req: Request):
    data = json.loads(await req.body())
    print("session: ", req.session)
    user_data = DB.authUser(
        username=data["username"], password=data["password"])
    req.session['user_info'] = user_data['data']
    res = JSONResponse(content=user_data, status_code=status.HTTP_202_ACCEPTED)
    return res


@app.post('/newuser')
async def handleNewUser(req: Request):
    data = json.loads(await req.body())
    user_data = DB.createNewUser(data)
    res = JSONResponse(content=user_data, status_code=status.HTTP_201_CREATED)
    return res


@app.websocket('/websocket_conn')
def handleWebSockets(req: Request):
    pass
