from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    username: str
    password: str
    real_name: str
    email: EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    real_name: str
