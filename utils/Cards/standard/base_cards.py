from typing import List
from typing import TYPE_CHECKING

from utils.LoggerManager import Logger
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
        self.status = 'ready'

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
        Logger.status(msg=f'{_data}.', tag='C_Card_Match')
        return _data

    # Movimentação

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        Logger.info(msg=f'O jogador {player.id} invocou a carta {
                    self.in_game_id}.', tag='C_Card_Match')
        if player.wisdom_available < self.wisdom_cost:
            return
        player.card_hand.remove(self)
        player.card_prepare_camp.append(self)
        self.status = "used"
        player.wisdom_available -= self.wisdom_cost

    async def onMoveToBattleZone(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        Logger.info(msg=f'O jogador {player.id} moveu a carta {
                    self.in_game_id} para Zona de Batalha.', tag='C_Card_Match')
        player.card_prepare_camp.remove(self)
        player.card_battle_camp.append(self)

    async def onRetreatToPrepareZone(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        Logger.info(msg=f'O jogador {player.id} recuou a carta {
                    self.in_game_id} para Zona de Preparação.', tag='C_Card_Match')

    # Habilidades

    async def addSkill(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        Logger.info(msg=f'O jogador {player.id} ativou habilidade da carta {
                    self.in_game_id}.', tag='C_Card_Match')

    async def rmvSkill(self, match: 'C_Match'):
        Logger.info(msg=f'A habilidade da carta {
                    self.in_game_id} foi removida.', tag='C_Card_Match')

    # Batalha

    async def onAttack(self, match: 'C_Match'):
        Logger.info(msg=f'A carta {
                    self.in_game_id} está atacando.', tag='C_Card_Match')

    async def onDefense(self, match: 'C_Match'):
        Logger.info(msg=f'A carta {
                    self.in_game_id} está defendendo.', tag='C_Card_Match')

    async def onDestroy(self, match: 'C_Match'):
        Logger.info(msg=f'A carta {
                    self.in_game_id} foi destruída.', tag='C_Card_Match')
        self.reset()

    async def hasSuccessfullyAttacked(
        self,
        match: 'C_Match',
        player: 'C_Player_Match' = None,
        player_target: 'C_Player_Match' = None,
    ):
        Logger.info(msg=f'A carta {self.in_game_id} atacou o jogador {
                    player_target.id}.', tag='C_Card_Match')

    async def hasNotSuccessfullyAttacked(
        self,
        match: 'C_Match',
        player: 'C_Player_Match' = None,
        player_target: 'C_Player_Match' = None,
    ):
        Logger.info(msg=f'A carta {
                    self.in_game_id} foi defendida.', tag='C_Card_Match')

    # Itemização

    async def onAttach(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        player.card_prepare_camp.remove(self)
        card_target.attached_cards.append(self)
        Logger.info(msg=f'O artefato {self.in_game_id} foi equipado ao Herói {card_target}.', tag='C_Card_Match')
        # Verificar a armadura de Deus

    async def onDettach(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attached_cards.remove(self)
        player.card_prepare_camp.append(self)
        Logger.info(msg=f'O artefato {self.in_game_id} foi removido do Herói {card_target}.', tag='C_Card_Match')

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
