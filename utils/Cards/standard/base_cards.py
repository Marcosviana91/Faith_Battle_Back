from typing import List
from typing import TYPE_CHECKING

from utils.console import consolePrint
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match, C_Player_Match


class C_Card_Match:
    def __init__(self, slug: str, in_game_id: str):
        self.slug = slug
        self.in_game_id = in_game_id

        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]
        self.attack_point = STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_point = STANDARD_CARDS_RAW_DATA[self.slug][3]
        self.card_type = STANDARD_CARDS_RAW_DATA[self.slug][4]

        self.status: str = 'ready'  # 'used' 'not-enuough'

        self.attached_cards: List[C_Card_Match] = []
        self.skill_focus_player_id: int = None  # skill da carta Davi

        self.imbloqueavel: bool = False
        self.indestrutivel: bool = False
        self.incorruptivel: bool = False

        self.increase_attack: int | None = 0
        self.increase_defense: int | None = 0

    def __str__(self):
        return f"{self.in_game_id}"

    def reset(self):
        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]
        self.attack_point = STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_point = STANDARD_CARDS_RAW_DATA[self.slug][3]

    def getStats(self):
        _data = {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "status": self.status,
        }
        if self.card_type == "hero":
            _attached_cards = []
            for card in self.attached_cards:
                _attached_cards.append(card.getStats())
            _data.update({
                "attack_point": self.attack_point,
                "defense_point": self.defense_point,
                "attached_cards": _attached_cards,
                "imbloqueavel": self.imbloqueavel,
                "indestrutivel": self.indestrutivel,
                "incorruptivel": self.incorruptivel,
            })
        return _data

    # Movimentação

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        if player.wisdom_available < self.wisdom_cost:
            return
        player.card_hand.remove(self)
        player.card_prepare_camp.append(self)
        self.status = "used"
        player.wisdom_available -= self.wisdom_cost

    async def onMoveToBattleZone(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        player.card_prepare_camp.remove(self)
        player.card_battle_camp.append(self)
        consolePrint.info(f'Jogador {player.id} moveu a carta {
                          self} para ZB.')

    async def onRetreatToPrepareZone(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        consolePrint.info(f'Jogador {player.id} recuou a carta {
                          self} para ZP.')

    # Habilidades

    async def addSkill(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        consolePrint.info(f'CARD: Adcionou skill de {self}')

    async def rmvSkill(self, match: 'C_Match'):
        consolePrint.info(f'CARD: Removeu skill de {self}')

    # Batalha

    async def onAttack(self, match: 'C_Match'):
        consolePrint.info(f'CARD: {self} está atacando')

    async def onDefense(self, match: 'C_Match'):
        consolePrint.info(f'CARD: {self} está defendendo')

    async def onDestroy(self, match: 'C_Match'):
        consolePrint.info(f'CARD: destruiu: {self}')
        self.reset()

    async def hasSuccessfullyAttacked(
        self,
        match: 'C_Match',
        player: 'C_Player_Match' = None,
        player_target: 'C_Player_Match' = None,
    ):
        consolePrint.info(
            f'CARD: {self} atacou com sucesso na sala {match.id} o jogador {player_target.id}!')

    async def hasNotSuccessfullyAttacked(
        self,
        match: 'C_Match',
        player: 'C_Player_Match' = None,
        player_target: 'C_Player_Match' = None,
    ):
        consolePrint.info(
            f'CARD: {self} foi defendido na sala {match.id} pelo jogador {player_target.id}!')

    # Itemização

    async def onAttach(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        player.card_prepare_camp.remove(self)
        card_target.attached_cards.append(self)
        consolePrint.info(f"O artefato {self} foi equipado ao Herói {
                          card_target}")
        # Verificar a armadura de Deus

    async def onDettach(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attached_cards.remove(self)
        player.card_prepare_camp.append(self)
        consolePrint.info(f"O artefato {self} foi removido do Herói {
                          card_target}")

# Utilitários


def getCardInListBySlugId(card_slug: str, card_list: List[C_Card_Match]) -> C_Card_Match | None:
    if card_slug != None:
        for card in card_list:
            if card != None:
                if card.in_game_id.find(card_slug) >= 0:
                    return card
    return None


def cardListToDict(card_list: list['C_Card_Match']):
    __list = []
    for card in card_list:
        if card:
            __list.append(card.getStats())
        else:
            __list.append({"slug": "not-defense"})
    return __list
