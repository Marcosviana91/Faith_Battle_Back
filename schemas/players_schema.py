from pydantic import BaseModel


STANDARD_CARDS = [
    'abraao', 'adao', 'daniel',
    'davi', 'elias', 'ester',
    'eva', 'jaco', "jose-do-egito",
    "josue", "maria", "moises",
    "noe", "salomao", "sansao",
]


class PlayersTinyDBSchema(BaseModel):
    __pydantic_post_init__ = "model_post_init"
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    available_cards: list[str] = STANDARD_CARDS
    xp_points: int = 0
    room_or_match_id: str = ""

    def model_post_init(
        self, *args, **kwargs,
    ):
        ...


class PlayersSchema(BaseModel):
    __pydantic_post_init__ = "model_post_init"
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    available_cards: list[str] = []
    xp_points: int = 0
    ready: bool = False
    card_deck: list[str] = []
    deck_try: int = 0
    card_hand: list = []

    def model_post_init(
        self, *args, **kwargs,
    ):
        self.card_deck = self.available_cards

# OK


class PlayersInMatchSchema(BaseModel):
    # __pydantic_post_init__ = 'model_post_init'

    id: int
    card_deck: list[str]
    card_hand: list
    card_prepare_camp: list = []
    card_battle_camp: list = []
    card_in_forgotten_sea: list = []
    faith_points: int
    wisdom_points: int = 0
    wisdom_used: int = 0
    # websocket: WebSocket = None
