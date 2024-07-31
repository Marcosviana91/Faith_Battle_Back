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

    def getPlayerStats(self, private: bool = False) -> dict:
        ...


class FightSchema:
    match_room: 'MatchSchema'
    fight_stage: int | None = 0
    player_attack: PlayersInMatchSchema
    attack_cards: list['CardSchema'] | None
    # attack_abilities: list[CardSchema] | None = []

    player_defense: PlayersInMatchSchema
    defense_cards: list['CardSchema'] | None = []
    # defense_abilities: list[CardSchema] | None = []


class MatchSchema:

    id: str = None
    start_match: str = None
    match_type: str = None
    players_in_match: list[PlayersInMatchSchema] = []
    round_match: int = 0
    player_turn: int = 0
    player_focus_id: int = 0
    can_others_move: bool = False
    fight_camp: FightSchema = None
    move_now: 'MoveSchema' = None
    
    def _getPlayerById(self, player_id: int) -> PlayersInMatchSchema | None:
        ...

    async def sendToPlayer(self, data: dict, player_id: int):
        ...

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        ...

    async def moveCard(self, player: PlayersInMatchSchema, card_id: str, move_from: str, move_to: str):
        ...
    
    def takeDamage(self, player: PlayersInMatchSchema, damage: int):
        ...


class MoveSchema(BaseModel):
    match_id: str
    round_match: int
    player_move: int
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive, done
    card_id: str | None = None
    player_target: int | None = None
    card_target: str | None = None
    card_list: list['CardSchema'] | None = []

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
    status: str | None = "ready"  # "ready" | "used" | "not-enough"

    card_type: str | None = None  # 'hero' | 'miracle' | 'sin' | 'artfacts' | 'legendary'

    increase_attack: int | None = 0
    increase_defense: int | None = 0
    skill_focus_player_id: int | None = None
    # used: bool
    # has_passive_skill: bool
    # has_active_skill: bool
    # attachable: bool

    @property
    def getCardStats(self):
        return {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "attack_point": self.attack_point,
            "defense_points": self.defense_points,
            "status": self.status,
        }

    def resetCardStats(self):
        print(f'Resetou {self.in_game_id}')

    def addSkill(self, player: PlayersInMatchSchema = None, match: MatchSchema = None):
        print(f'Adcionou skill de {self.in_game_id}')

    def rmvSkill(self, player: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        print(f'Removeu skill de {self.in_game_id}')

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        player.card_hand.remove(self)
        player.card_prepare_camp.append(self)
        print(f'invocou: {self}')
        if self.card_type == 'hero':
            print('é heroi')
            if getCardInListBySlugId('abraao', player.card_battle_camp):
                print('tem abraao')
                print(f"player {player.id} ativou abraão")
                player.faith_points += 1

    def onDestroy(self, player: PlayersInMatchSchema, match: MatchSchema):
        print(f'destruiu: {self.in_game_id}')

    def onAttack(
        self,
        player: PlayersInMatchSchema,
        match: MatchSchema,
        player_target: PlayersInMatchSchema | None = None
    ):
        print(f'{self.in_game_id} está atacando')

    def onDefense(
        self,
        player: PlayersInMatchSchema,
        match: MatchSchema,
        player_target: PlayersInMatchSchema | None = None
    ):
        print(f'{self.in_game_id} está defendendo')


def getCardInListBySlugId(card_slug: str, card_list: list[CardSchema]) -> CardSchema | None:
    for card in card_list:
        if card.in_game_id.find(card_slug) >= 0:
            return card
    return None
