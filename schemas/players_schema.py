from pydantic import BaseModel


class PlayersSchema(BaseModel):
    __pydantic_post_init__ = "model_post_init"
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    available_cards: list[str]
    xp_points: int = 0
    ready: bool = False
    card_deck: list[str] = []
    deck_try: int = 0
    card_hand: list = []

    def model_post_init(
        self, *args, **kwargs,
    ):
        self.card_deck = self.available_cards

    def onJoinMatch(self):
        ...

    def onEndMatch(self):
        ...

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
