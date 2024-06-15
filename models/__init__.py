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
        ...

    def onLogout(self):
        ...


class Player(SQLModel, table=True):
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int = Field(primary_key=True, foreign_key='user.id')
    xp_points: int = Field(default=0)
    available_cards: int = Field(foreign_key='player_cards.owner_id')
    decks: int = Field(foreign_key='player_decks.id')
    # matches: int = Field(foreign_key='players_in_match.player_id')

    def onJoinMatch(self):
        ...

    def onEndMatch(self):
        ...


class Card(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    # nome único: jose-do-egito
    card_slug: str
    # hero, artifacts, miracles, sins, legendary, wisdom
    in_game_id: str
    card_type: int = Field(foreign_key='cards_type.id')
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

    def __str__(self):
        return f'{self.card_name}, {self.card_wisdom_cost}, {self.card_attack_points}, {self.card_defense_points}'

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


class Cards_Type(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    type_name: str  # hero, artifacts, miracles, sins, legendary, wisdom
    type_description: str


class Player_Cards(SQLModel, table=True):
    '''
    Tablela de Relação Many-to-Many\n
    Relação de Todas as cartas que um jogador possui
    '''
    owner_id: int = Field(primary_key=True, foreign_key='player.id')
    card_id: int = Field(foreign_key='card.id')


class Player_Decks(SQLModel, table=True):
    '''
    Tablela de Relação Many-to-Many\n
    Relação de Todas as cartas que um jogador quer usar em uma partida
    '''
    id: Optional[int] = Field(primary_key=True)
    owner_id: int = Field(foreign_key='player.id')
    card_id: int = Field(foreign_key='card.id')
    deck_name: str


class Match(SQLModel, table=True):
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


class Match_Types(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    type_name: str  # Survival, Coop
    type_description: str


class Moves_in_Match(SQLModel, table=True):
    '''
    Tablela de Relação Many-to-Many\n
    Relação de movimentos em uma partida
    '''
    # id: Optional[int] = Field(primary_key=True)
    moved_at: datetime = Field(default=datetime.now())

    match_id: int = Field(primary_key=True, foreign_key='match.id')
    # match: Match = Relationship(back_populates='moves_in_this_match')

    player_id_move: int = Field(foreign_key='player.id')
    card_id_move: int = Field(foreign_key='card.id')
    player_id_target: int = Field(foreign_key='player.id')
    # Carta alvo, opcional / Uma carta pode ser lançada diretamente contra um jogador sem mirar qualquer carta.
    card_id_target: Optional[int] = Field(foreign_key='card.id')


# Pydantic BaseModel
class Statistics(SQLModel):
    id: Optional[int] = Field(primary_key=True)
