from pydantic import BaseModel

from schemas.cards_schema import CardSchema
from utils.Cards import cardListToDict, ALL_CARDS


class PlayersTinyDBSchema(BaseModel):
    __pydantic_post_init__ = "model_post_init"
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    available_cards: list[str] = ALL_CARDS
    xp_points: int = 0
    room_or_match_id: str = ""

    def model_post_init(
        self, *args, **kwargs,
    ):
        ...

# REMOVER DAQUI PRA BAIXO

class PlayersSchema(BaseModel):
    __pydantic_post_init__ = "model_post_init"
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''
    id: int
    available_cards: list[CardSchema] = []
    xp_points: int = 0
    ready: bool = False
    card_deck: list[CardSchema] = []
    deck_try: int = 0
    card_hand: list[CardSchema] = []

    def model_post_init(
        self, *args, **kwargs,
    ):
        self.card_deck = self.available_cards

    @property
    def getPlayersStats(self):
        return {
            "id": self.id,
            "ready": self.ready,
            "xp_points": self.xp_points,
            "card_deck": cardListToDict(self.card_deck),
            "card_hand": cardListToDict(self.card_hand),
        }



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
    wisdom_available: int = 0

    #
    # lista com id de jogadores q o jogador atual já atacou
    ja_atacou: list[int] = []
    fe_inabalavel: bool = False
    incorruptivel: bool = False
    nao_sofre_danos_de_efeitos: bool = False
    nao_sofre_ataque_de_herois: bool = False

    def getPlayerStats(self, private: bool = False) -> dict:
        # private são os dados que só o jogador precisa saber
        if private:
            return {
                "id": self.id,
                "card_hand": cardListToDict(self.card_hand),
                "faith_points": self.faith_points,
                "wisdom_points": self.wisdom_points,
                "wisdom_available":  self.wisdom_available,
                "ja_atacou": self.ja_atacou,
                "fe_inabalavel": self.fe_inabalavel,
                "incorruptivel": self.incorruptivel,
                "nao_sofre_danos_de_efeitos": self.nao_sofre_danos_de_efeitos,
                "nao_sofre_ataque_de_herois": self.nao_sofre_ataque_de_herois,
            }
        return {
            "id": self.id,
            "card_deck": cardListToDict(self.card_deck),
            "card_prepare_camp": cardListToDict(self.card_prepare_camp),
            "card_battle_camp": cardListToDict(self.card_battle_camp),
            "card_in_forgotten_sea": cardListToDict(self.card_in_forgotten_sea),
            "faith_points": self.faith_points,
            "wisdom_points": self.wisdom_points,
            "wisdom_available":  self.wisdom_available,
            "fe_inabalavel": self.fe_inabalavel,
            "incorruptivel": self.incorruptivel,
            "nao_sofre_danos_de_efeitos": self.nao_sofre_danos_de_efeitos,
            "nao_sofre_ataque_de_herois": self.nao_sofre_ataque_de_herois,
        }
