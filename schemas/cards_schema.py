from pydantic import BaseModel, ConfigDict

from utils.console import consolePrint


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

    #
    fe_inabalavel: bool = False
    incorruptivel: bool = False
    nao_sofre_danos_de_efeitos: bool = False
    nao_sofre_ataque_de_herois: bool = False

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

    async def moveCard(self, player: PlayersInMatchSchema, card_id: str, move_from: str, move_to: str) -> bool:
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
    player_target2: int | None = None
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
    attachable: bool = False
    attached_cards: list = []
    increase_attack: int | None = 0
    increase_defense: int | None = 0
    skill_focus_player_id: int | None = None  # Usado por Davi

    #
    imbloqueavel: bool = False
    indestrutivel: bool = False 
    incorruptivel: bool = False # não é atingido por pecados

    def getCardStats(self):
        _data = {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "attack_point": self.attack_point,
            "defense_points": self.defense_points,
            "status": self.status,
            "attachable": self.attachable,
            "imbloqueavel": self.imbloqueavel,
            "indestrutivel": self.indestrutivel,
            "incorruptivel": self.incorruptivel,
        }
        return _data

    def resetCardStats(self):
        print(f'Resetou {self.in_game_id}')

# Movimentação

    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        player.card_hand.remove(self)
        player.card_prepare_camp.append(self)
        consolePrint.info(f'CARD: invocou: {self}')
        self.status = "used"
        if self.card_type == 'miracle':
            await match.sendToPlayer(
                data={
                    "data_type": "card_skill",
                    "card_data": {
                        "slug": self.slug,
                    }
                },
                player_id=player.id
            )
        if self.card_type == 'artifact':
            self.status = 'ready'

    async def onMoveToAttackZone(self, match: MatchSchema | None):
        player = match._getPlayerById(match.move_now.player_move)
        consolePrint.info(f'Jogador {player.id} moveu a carta {
                          self.in_game_id} para ZB.')

    async def onRetreatToPrepareZone(self, match: MatchSchema | None):
        player = match._getPlayerById(match.move_now.player_move)
        consolePrint.info(f'Jogador {player.id} recuou a carta {
                          self.in_game_id} para ZP.')


# Habilidades


    async def addSkill(self, match: MatchSchema | None = None):
        consolePrint.info(f'CARD: Adcionou skill de {self.in_game_id}')
        player = match._getPlayerById(match.move_now.player_move)
        if self.card_type == 'miracle':
            await match.moveCard(player, self.in_game_id, "prepare", "forgotten")

    async def rmvSkill(self, match: MatchSchema | None = None):
        consolePrint.info(f'CARD: Removeu skill de {self.in_game_id}')


# Itemização


    async def onAttach(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        player.card_prepare_camp.remove(self)
        card_target.attached_cards.append(self)
        consolePrint.info(f"O artefato {self.in_game_id} foi equipado ao Herói {
                          card_target.in_game_id}")
        # Verificar a armadura de Deus

    async def onDettach(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attached_cards.remove(self)
        player.card_prepare_camp.append(self)
        consolePrint.info(f"O artefato {self.in_game_id} foi removido do Herói {
                          card_target.in_game_id}")


# Batalha


    async def onDestroy(self, match: MatchSchema | None = None):
        consolePrint.info(f'CARD: destruiu: {self.in_game_id}')

    async def onAttack(self, match: MatchSchema | None = None):
        consolePrint.info(f'CARD: {self.in_game_id} está atacando')

    async def onDefense(self, match: MatchSchema | None = None):
        consolePrint.info(f'CARD: {self.in_game_id} está defendendo')

    async def hasSuccessfullyAttacked(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        defense_cards: list['CardSchema'] | None = None,
        match: MatchSchema | None = None,
    ):
        consolePrint.info(
            f'CARD: {self.in_game_id} atacou com sucesso na sala {match.id}!')

    async def hasNotSuccessfullyAttacked(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        defense_cards: list['CardSchema'] | None = None,
        match: MatchSchema | None = None,
    ):
        consolePrint.info(
            f'CARD: {self.in_game_id} foi defendido na sala {match.id}!')

# Utilidade


def getCardInListBySlugId(card_slug: str, card_list: list[CardSchema]) -> CardSchema | None:
    if card_slug != None:
        for card in card_list:
            if card != None:
                if card.in_game_id.find(card_slug) >= 0:
                    return card
    return None
