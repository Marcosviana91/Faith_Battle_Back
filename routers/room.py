from fastapi import APIRouter, HTTPException, status

from schemas.API_schemas import APIResponseSchema
from schemas import PlayersSchema
from schemas import RoomSchema
from utils.ROOM.RoomManager import RM

router = APIRouter(prefix="/room", tags=["room"])


@router.get('/')
def getRoomList():
    rooms = RM.getAllRoomsStats()
    response = APIResponseSchema(message="There's no room.")
    if rooms == False:
        return response
    response.data_type = "room_list"
    response.room_list = rooms
    return response


@router.post('/')
async def createRoom(new_room: RoomSchema):
    response = APIResponseSchema()
    room = await RM.createRoom(new_room)
    response.data_type = "room_data"
    response.room_data = room
    return response


@router.post('/{room_id}/')
async def enterRoom(room_id: str, player:PlayersSchema, password:str = ""):
    response = APIResponseSchema(message='Something goes wrong')
    try:
        room = await RM.enterRoom(room_id, player, password)
        response.data_type = "room_data"
        response.room_data = room
        return response
    except Exception as e:
        print(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
