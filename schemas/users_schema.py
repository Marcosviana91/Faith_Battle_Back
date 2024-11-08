from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict, EmailStr


class AuthSchema(BaseModel):
    username: str
    password: str


class NewUserSchema(BaseModel):
    username: str
    password: str
    first_name: str
    avatar: int
    # email: EmailStr


class UserWs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    access_token: str
    websocket: WebSocket = None
    
    
class UserData(BaseModel):
    id: int
    last_login: str
    username: str
    email: str
    first_name: str
    avatar: str

    
class PlayerData(BaseModel):
    id: int
    avatar: str
    available_cards: list[str]
    # decks: list[Deck] | None
    selected_deck: str | None
    xp_points: int
    room_id: str | None
    match_id: str | None
