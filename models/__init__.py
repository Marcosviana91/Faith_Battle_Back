from typing import Optional, ClassVar
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    '''
    Dados de identificação do usuário para login
    '''
    id: Optional[int] = Field(primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    last_login: datetime = Field(default=datetime.now())

    username: str = Field(index=True)
    password: str
    real_name: str
    email: str

    def __init__(self, username, password, real_name, email):
        self.username = username
        self.password = password
        self.real_name = real_name
        self.email = email

    def onLogin(self):
        self.last_login = datetime.now()

    def onLogout(self):
        ...


# Salvo em Tiny DB
class Player(SQLModel):
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    xp_points: int
    available_cards: list[str]

    def __init__(self, id: int):
        self.id = id
        self.xp_points = 0
        self.available_cards = [
            'abraao', 'adao', 'daniel',
            'davi', 'elias', 'ester',
            'eva', 'jaco', "jose-do-egito",
            "josue", "maria", "moises",
            "noe", "salomao", "sansao"
        ]

    def onJoinMatch(self):
        ...

    def onEndMatch(self):
        ...


# Schema Não vai pro DB
class Card():
    id: Optional[int] = Field(primary_key=True)
    # nome único: jose-do-egito
    card_slug: str
    # player id - card slug - secret
    in_game_id: str
    # hero, artifacts, miracles, sins, legendary, wisdom
    card_name: str
    card_description: str
    card_holy_reference: str
    card_image: str
    card_wisdom_cost: int
    card_attack_points: int = Field(default=0)
    card_defense_points: int = Field(default=0)
    card_has_passive_skill: bool = Field(default=False)
    card_has_active_skill: bool = Field(default=False)
    card_attachable: bool = Field(default=False)

    ready: bool

    def __init__(self, in_game_id: str):
        self.in_game_id = in_game_id

    def __str__(self):
        return f'\n########\n{self.card_slug}: {self.in_game_id}\n{self.card_wisdom_cost}, {self.card_attack_points}, {self.card_defense_points}\n########\n'

    def passiveSkill(self):
        ...

    def activeSkill(self):
        ...

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    def onDestroy(self):
        ...

    def onInvoke(self):
        ...

    def onAttack(self):
        ...

    def onDefense(self):
        ...


class Cards_Type():
    id: Optional[int] = Field(primary_key=True)
    type_name: str  # hero, artifacts, miracles, sins, legendary, wisdom
    type_description: str


class Match():
    id: Optional[int] = Field(primary_key=True)
    start_match: datetime | None = Field(default=None)
    end_match: datetime | None = Field(default=None)
    created_by: int
    room_name: str
    max_players: int
    match_type: int = Field(foreign_key='match_types.id')
    password: str

    # Jogadores na partida (2 - 8)
    players_in_match: ClassVar[list] = []
    # players_in_match: list['User'] = Relationship()
    # # Movimentos da nesta partida
    moves_in_match: ClassVar[list] = []
    # moves_in_match: list["Moves"] = Relationship()

    def joinTheMatch(self, player_id: int):
        self.players_in_match.append(player_id)

    def leftTheMatch(self, player_id: int):
        self.players_in_match.remove(player_id)

    def newMove(self, move_data):
        ...


# Pydantic BaseModel
class Statistics(SQLModel):
    id: Optional[int] = Field(primary_key=True)
