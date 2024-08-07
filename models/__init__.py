from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    """
    Dados de identificação do usuário para login
    """

    __tablename__ = "user"
    id: Optional[int] = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    last_login: datetime = Field(default=datetime.now())

    username: str = Field(index=True)
    password: str
    real_name: str
    # email: str
    avatar: int

    # def __init__(self, username, password, real_name, email):
    def __init__(self, username, password, real_name, avatar):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.avatar = avatar
        # self.email = email

    def onLogin(self):
        self.last_login = datetime.now()

    def onLogout(self): ...
