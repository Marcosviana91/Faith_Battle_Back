from pydantic import BaseModel
from .users_schema import UserPublic


class APIResponseSchema(BaseModel):
    message: str
    data_type: str | None = "error"
    user_data: UserPublic | None = None
