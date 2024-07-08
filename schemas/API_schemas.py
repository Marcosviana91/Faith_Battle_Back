from pydantic import BaseModel
from .users_schema import UserPublic
from .games_schema import RoomSchema


class APIResponseSchema(BaseModel):
    message: str
    data_type: str | None = "error"
    user_data: UserPublic | None = None
    room_list: list | None = None
    room_data: RoomSchema | None = None
    
class ClientRequestSchema(BaseModel):
    data_type: str
    user_data: dict | None = None
    room_data: RoomSchema | None = None

