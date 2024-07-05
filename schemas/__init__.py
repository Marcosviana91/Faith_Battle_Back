from pydantic import BaseModel, EmailStr

# Used in TinyDB and JSON schemas


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


class APIResponseSchema(BaseModel):
    message: str
    data_type: str | None = "error"
    user_data: UserPublic | None = None


class User:
    """
    Dados de identificação do usuário para login
    """

    def __init__(
        self,
        id: int | None,
        username: str | None,
        password: str | None,
        created_at: str | None,
        last_login: str | None,
        real_name: str | None,
        email: str | None,
    ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.last_login = last_login
        self.real_name = real_name
        self.email = email


# Salvo em Tiny DB


class Player:
    """
    Dados do usuário, relativos ao jogo (como jogador)
    """

    def __init__(
        self, id: int, xp_points: int = 0, available_cards: list[str] = []
    ):
        self.id = id
        self.xp_points = xp_points
        self.available_cards = (
            [
                "abraao",
                "adao",
                "daniel",
                "davi",
                "elias",
                "ester",
                "eva",
                "jaco",
                "jose-do-egito",
                "josue",
                "maria",
                "moises",
                "noe",
                "salomao",
                "sansao",
            ]
            if available_cards == []
            else available_cards
        )

    def onJoinMatch(self): ...

    def onEndMatch(self): ...


class APIResponseProps:
    def __init__(
        self,
        message: str | None,
    ):
        self.message = message
        self.data_type = "error"
        self.user_data: dict = {}
        self.room_data: dict = {}
        self.room_list: list = []
        self.player_data: dict = {}
        # self.player_in_match_data: Players_in_Match = None
        # self.card_data: Card = None
        # self.game_data: GameData = None

    # @property
    # def __dict__(self):
    #     __temp = {
    #         "data_type": self.data_type,
    #         "user_data": self.user_data,
    #         "room_data": self.room_data,
    #         "player_data": self.player_data,
    #     }
    #     __reponse = {}

    #     for k, v in __temp.items():
    #         if v:
    #             __reponse[k] = v

    #     return __reponse


class ClientRequestProps:
    def __init__(
        self,
        **kwargs,
    ):
        # print(__file__,'\nClientRequestProps.__init__\n' ,kwargs)
        self.data_type: str = kwargs.get("data_type")
        self.user_data: dict = kwargs.get("user_data")  # User
        self.room_data: dict = kwargs.get("room_data")
        self.player_data: dict = kwargs.get("player_data")
        # self.player_in_match_data: dict = kwargs.get("player_in_match_data")
        # self.card_data: dict = kwargs.get("card_data")
        # self.game_data: dict = kwargs.get("game_data")

    @property
    def __dict__(self):
        __temp = {
            "data_type": self.data_type,
            "user_data": self.user_data,
            "room_data": self.room_data,
            "player_data": self.player_data,
        }
        __reponse = {}

        for k, v in __temp.items():
            if v:
                __reponse[k] = v

        return __reponse
