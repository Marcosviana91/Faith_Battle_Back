from pydantic import BaseModel


class CardSchema(BaseModel):

    # nome único: jose-do-egito
    slug: str | None
    wisdom_cost: int | None = None
    attack_point: int | None = None
    defense_point: int | None = None
    # player id - card slug - secret
    in_game_id: str | None = None
    status: str | None = "ready"  # "ready" | "used" | "not-enough"

    card_type: str | None = None  # 'hero' | 'miracle' | 'sin' | 'artfacts' | 'legendary'
    attachable: bool = False
    attached_cards: list = []
    increase_attack: int | None = 0
    increase_defense: int | None = 0
    skill_focus_player_id: int | None = None  # Usado por Davi

    #
    imbloqueavel: bool = False
    indestrutivel: bool = False
    incorruptivel: bool = False  # não é atingido por pecados


class PlayersSchema(BaseModel):
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    # deck: list[str]
    # xp_points: int
    # ready: bool = False
    # card_deck: list[CardSchema] = []
    # deck_try: int = 0
    # card_hand: list[CardSchema] = []


class RoomSchema(BaseModel):
    id: str = None
    name: str
    created_by: PlayersSchema

    connected_players: list[list[PlayersSchema]] = []
    max_players: int = 2
    teams: int = 1
    password: str = None
