from pydantic import BaseModel, EmailStr, ConfigDict
from fastapi import WebSocket


class AuthSchema(BaseModel):
    username: str
    password: str


class NewUserSchema(BaseModel):
    username: str
    password: str
    real_name: str
    email: EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    real_name: str


class UserWs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int
    token: str
    websocket: WebSocket = None
