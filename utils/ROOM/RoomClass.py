
from nanoid import generate

from utils.Cards import cardListToDict
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

MINIMUM_DECK_CARDS = 10
MAXIMUM_CARDS_REPEATS = 2
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15
MAXIMUM_DECK_TRIES = 3


class C_Card:
    def __init__(self, slug: str, player_id: int):
        self.slug =slug
        
        self.wisdom_cost: int | None = None
        self.card_type: str = None
        
        self.in_game_id = generate(size=6)
        self.status: str = 'ready' # 'used' 'not-enuough'
        
    def reset(self):
        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]

    def getStats(self):
        return {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "status": self.status,
        }
        
class C_Hero(C_Card):
    def __init__(self, slug):
        super().__init__(slug)
        self.card_type = 'hero'
        self.attack_point: int = 0
        self.defense_points: int = 0
        self.imbloqueavel: bool = False
        self.indestrutivel: bool = False
        self.incorruptivel: bool = False

    def reset(self):
        super().reset()
        self.attack_point =  STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_points =  STANDARD_CARDS_RAW_DATA[self.slug][3]
        
    def getStats(self):
        _data = super().getStats()
        _data.update({
            "attack_point": self.attack_point,
            "defense_points": self.defense_points,
            "imbloqueavel": self.imbloqueavel,
            "indestrutivel": self.indestrutivel,
            "incorruptivel": self.incorruptivel,
        })
        
class C_Miracle(C_Card):
    def __init__(self, slug):
        super().__init__(slug)
        self.card_type = 'miracle'
        
class C_Artifacts(C_Card):
    def __init__(self, slug):
        super().__init__(slug)
        self.card_type = 'miracle'


class C_Player:
    def __init__(self, id: int):
        self.id: int = id
        self.ready: bool = False
        self.xp_points: int = 0
        self.deck_try: int = 0

        self.available_cards: list[str] = []
        self.card_deck: list[C_Card] = []
        self.card_hand: list[C_Card] = []
        self.card_prepare_camp: list[C_Card] = []
        self.card_battle_camp: list[C_Card] = []
        self.card_in_forgotten_sea: list[C_Card] = []

        self.faith_points: int = 0
        self.wisdom_points: int = 0
        self.wisdom_available: int = 0

        self.ja_atacou: list[int] = []
        self.fe_inabalavel: bool = False
        self.incorruptivel: bool = False
        self.nao_sofre_danos_de_efeitos: bool = False
        self.nao_sofre_ataque_de_herois: bool = False

    def getStats(self, type: str = None):

        _data = {
            'id': self.id,
            'ready': self.ready,
            'xp_point': self.xp_points,
            'card_deck': cardListToDict(self.card_deck),
            'card_hand': cardListToDict(self.card_hand),
        }

        match (type):
            case 'match':
                _data.update({
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
                })
            case 'my_self':
                _data.pop("card_deck")
                _data.pop("xp_point")

        return _data


class C_Team:
    def __init__(self, name: str):
        self.name = name
        self.members = list[C_Player]

    def join(self, player: C_Player) -> str:
        self.members.append(player)

    def left(self, player: C_Player) -> str:
        self.members.remove(player)

    def getStats(self):
        ...


class C_Room:
    def __init__(
        self,
        room_name: str,
        game_type: str = 'survival',
        max_player: int = 2,
        password: str = "",
    ) -> str:
        self.room_name = room_name,
        self.game_type = game_type,
        self.max_player = max_player,
        self.password = password,

        self.id = generate(size=12)
        self.room_stage = 0

        self.setConfig()
        return self.id

    def setConfig(
        self,
        minimum_deck_cards: int = MINIMUM_DECK_CARDS,
        maximum_cards_repeats: int = MAXIMUM_CARDS_REPEATS,
        faith_points: int = MAXIMUM_FAITH_POINTS,
        initial_cards: int = INITIAL_CARDS,
        maximum_deck_tries: int = MAXIMUM_DECK_TRIES,
    ):
        self.minimum_deck_cards = minimum_deck_cards
        self.maximum_cards_repeats = maximum_cards_repeats
        self.faith_points = faith_points
        self.initial_cards = initial_cards
        self.maximum_deck_tries = maximum_deck_tries

        return {
            'minimum_deck_cards': self.minimum_deck_cards,
            'maximum_cards_repeats': self.maximum_cards_repeats,
            'faith_points': self.faith_points,
            'initial_cards': self.initial_cards,
            'maximum_deck_tries': self.maximum_deck_tries,
        }

    def getStats(self) -> dict:
        return {
            'id': self.id,
            'room_name': self.room_name,
        }
