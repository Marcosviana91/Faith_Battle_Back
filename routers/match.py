from fastapi import APIRouter, Depends, HTTPException, status

from fastapi.responses import JSONResponse
from fastapi.requests import Request

# from utils import ROOMS

router = APIRouter(prefix="/match", tags=["match"])


@router.get('/')
def handleMatchList(req: Request):
    # rooms = ROOMS.getAllRoomsInfo()
    # response = JSONResponse(content=rooms.__dict__)
    return {"response": "0 ROOMS"}


# @router.get('/{room_id}')
# def handleMatchById(req: Request, room_id: str):
#     print(room_id)
#     room_info = ROOMS.getRoomInfoById(room_id)
#     res = JSONResponse(content=room_info)
#     return res


# @router.get('/{room_id}/{player_id}')
# def handlePlayerInMatch(req: Request, room_id: str, player_id: str):
#     room_info = ROOMS.getPlayerInRoomInfoById(room_id, player_id)
#     res = JSONResponse(content=room_info)
#     return res
