from fastapi import APIRouter, HTTPException, status

from schemas.API_schemas import APIResponseSchema
from schemas.players_schema import PlayersSchema
from schemas.rooms_schema import RoomSchema
from utils.ROOM.RoomManager import ROOMS

router = APIRouter(prefix="/room", tags=["room"])


@router.get('/')
def getRoomList():
    rooms = ROOMS.getAllRoomsInfo()
    response = APIResponseSchema(message="There's no room.")
    if rooms == False:
        return response
    response.message = f"Rooms founds: {len(rooms)}"
    response.data_type = "room_list"
    response.room_list = rooms
    return response


@router.post('/')
def createRoom(new_room: RoomSchema):
    response = APIResponseSchema(message='Something goes wrong')
    room = ROOMS.createRoom(new_room)
    response.message = f"room created: {room['id']}"
    response.data_type = "room_data"
    response.room_data = room
    return response


@router.post('/{room_id}/')
async def enterRoom(room_id: str, player:PlayersSchema, password:str = ""):
    response = APIResponseSchema(message='Something goes wrong')
    try:
        room = await ROOMS.enterRoom(room_id, player, password)
        response.message = "room_connected"
        response.data_type = "room_data"
        response.room_data = room
        return response
    except Exception as e:
        print(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}"
        )
