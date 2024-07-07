from fastapi import APIRouter

from schemas import APIResponseSchema, RoomSchema
from utils import ROOMS

router = APIRouter(prefix="/room", tags=["room"])


@router.get('/')
def getRoomList():
    rooms = ROOMS.getAllRoomsInfo()
    response = APIResponseSchema(message="There's no room.")
    if rooms == False:
        return response
    response.message = f"Rooms founds: {len(rooms)}"
    response.data_type = "rooms_list"
    response.rooms_list = rooms
    return response


@router.post('/')
def createRoom(new_room: RoomSchema):
    response = APIResponseSchema(message='Something goes wrong')
    room = ROOMS.addRoom(new_room)
    response.message = f"room created: {room.id}"
    response.data_type = "room_data"
    response.room_data = room
    return response
