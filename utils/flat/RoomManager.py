from nanoid import generate


class C_RoomFlat:
    def __init__(
        self,
        name: str,
        max_players: int = 2,
        password: str = "",
        created_by: dict = {},
        *args, **kwargs
    ):
        self.name = name
        self.max_players = max_players
        self.password = password
        self.id = generate(size=12)
        self.created_by = created_by

    async def connect(self, player_id: int = None, password: str = None):
            assert password == self.password
            