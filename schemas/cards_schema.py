from pydantic import BaseModel, ConfigDict


class PlayersInMatchSchema:
    id: int
    card_deck: list['CardSchema']
    card_hand: list['CardSchema']
    card_prepare_camp: list['CardSchema'] = []
    card_battle_camp: list['CardSchema'] = []
    card_in_forgotten_sea: list['CardSchema'] = []
    faith_points: int
    wisdom_points: int = 0
    wisdom_available: int = 0

    @property
    def getPlayerStats(self):
        ...

class MatchSchema:

    id: str = None
    start_match: str = None
    match_type: str = None
    players_in_match: list[PlayersInMatchSchema] = []
    round_match: int = 0
    player_turn: int = 0
    player_focus_id: int = 0
    can_others_move: bool = False

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        ...
    def moveCard(self, player: PlayersInMatchSchema, card_id: str, move_from: str, move_to: str):
        ...

##################################################################

class CardSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # nome único: jose-do-egito
    slug: str | None
    wisdom_cost: int | None = None
    attack_point: int | None = None
    defense_points: int | None = None
    # player id - card slug - secret
    in_game_id: str | None = None
    status: str | None = "ready" #"ready" | "used" | "not-enough"

    # card_type: int

    # used: bool
    # has_passive_skill: bool
    # has_active_skill: bool
    # attachable: bool

    @property
    def getCardStats(self):
        return {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "wisdom_cost": self.wisdom_cost,
            "attack_point": self.attack_point,
            "defense_points": self.defense_points,
            "status": self.status,
        }


    def passiveSkill(self):
        ...

    def activeSkill(self):
        ...

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        print(f'invocou: {self.in_game_id}')

    def onDestroy(self):
        ...

    def onAttack(self):
        ...

    def onDefense(self):
        ...

