from pydantic import BaseModel

from .rooms_schema import RoomSchema


class APIResponseSchema(BaseModel):
    message: str
    data_type: str | None = "error"
    user_data: dict | None = None
    room_list: list | None = None
    room_data: dict | None = None #OK

class ClientRequestSchema(BaseModel):
    data_type: str
    user_data: dict | None = None
    room_data: dict | None = None
    retry_cards: list | None = None
    match_move: dict | None = None

