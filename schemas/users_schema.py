from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict, EmailStr


class AuthSchema(BaseModel):
    username: str
    password: str


class NewUserSchema(BaseModel):
    username: str
    password: str
    real_name: str
    avatar: int
    # email: EmailStr
    
class UpdateUserSchema(BaseModel):
    id: int
    username: str
    password: str
    real_name: str
    avatar: int
    token:str
    # email: EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    # email: EmailStr
    real_name: str
    avatar: int
    available_cards: list[str] | None = []
    xp_points: int | None = 0


class UserWs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    token: str
    websocket: WebSocket = None
