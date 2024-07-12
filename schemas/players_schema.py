from pydantic import BaseModel
from schemas.cards_schema import CardSchema


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
    card_hand: list[str] = []

    def model_post_init(
        self, *args, **kwargs,
    ):
        self.card_deck = self.available_cards

# OK


class PlayersInMatchSchema(BaseModel):
    # __pydantic_post_init__ = 'model_post_init'

    id: int
    card_deck: list[CardSchema]
    card_hand: list[CardSchema]
    card_prepare_camp: list[CardSchema] = []
    card_battle_camp: list[CardSchema] = []
    card_in_forgotten_sea: list[CardSchema] = []
    faith_points: int
    wisdom_points: int = 0
    wisdom_used: int = 0
    
    @property
    def getPlayerStats(self):
        def a(card_list:list[CardSchema]):
            __list = []
            for card in card_list:
                __list.append(card.getCardStats)
            return __list
        return {
                "id": self.id,
                "card_hand": a(self.card_hand),  # REMOVER
                "card_deck": a(self.card_deck),  # REMOVER
                "card_prepare_camp": a(self.card_prepare_camp),
                "card_battle_camp": a(self.card_battle_camp),
                "card_in_forgotten_sea": a(self.card_in_forgotten_sea),
                "faith_points": self.faith_points,
                "wisdom_points": self.wisdom_points,
                "wisdom_used":  self.wisdom_used
            }
