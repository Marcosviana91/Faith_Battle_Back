from fastapi import WebSocket
from pydantic import BaseModel, ConfigDict, EmailStr


class AuthSchema(BaseModel):
    username: str
    password: str


class NewUserSchema(BaseModel):
    username: str
    password: str
    first_name: str
    avatar: str
    # email: EmailStr


class UserWs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    access_token: str
    websocket: WebSocket = None
