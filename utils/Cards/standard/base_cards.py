from typing import TYPE_CHECKING, List, Dict

from nanoid import generate

from utils.Notification import Notification
from utils.LoggerManager import Logger
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match, C_Player_Match, MoveSchema


class C_Card_Room:
    def __init__(self, slug: str, player_id: int):
        self.slug = slug

        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]
        self.attack_point = STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_point = STANDARD_CARDS_RAW_DATA[self.slug][3]
        self.card_type = STANDARD_CARDS_RAW_DATA[self.slug][4]

        self.in_game_id = f'{player_id}_{slug}_{generate(
            size=6, alphabet='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')}'

    def __str__(self):
        return f"{STANDARD_CARDS_RAW_DATA[self.slug][0]}"

    def getStats(self):
        return {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "attack_point": self.attack_point,
            "defense_point": self.defense_point,
            "status": 'ready',
        }


class C_Card_Move:
    def __init__(
        self,
        player_target_id: int | None = None,
        player_target2_id: int | None = None,
        card_target_id: str | None = None,
        card_list: List[Dict] | None = [],
        *args, **kwargs
    ):
        self.player_target_id = player_target_id,
        self.player_target2_id = player_target2_id,
        self.card_target_id = card_target_id,
        self.card_list = card_list


class C_Card_Match:
    def __init__(self, slug: str, in_game_id: str):
        self.slug = slug
        self.in_game_id = in_game_id
        self.player: C_Player_Match = None

        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]
        self.attack_point = STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_point = STANDARD_CARDS_RAW_DATA[self.slug][3]
        self.card_type = STANDARD_CARDS_RAW_DATA[self.slug][4]

        self.status: str = 'ready'  # 'used', 'not-enuough'
        self.can_attack: bool = False
        self.can_move: bool = True

        self.attached_cards: List[C_Card_Match] = []  # Equipamentos acoplados
        self.attached_effects: List[C_Card_Match] = []  # Efeitos vigentes

        self.skill_focus_player_id: int = None  # skill da carta Davi
        # dados do movimento da carta, para quando for realizado de fato
        self.card_move: C_Card_Move = None

        self.imbloqueavel: bool = False
        self.indestrutivel: bool = False
        self.incorruptivel: bool = False

        # Usado por Daniel
        self.increase_attack: int | None = 0
        self.increase_defense: int | None = 0

    def __str__(self):
        return f"{STANDARD_CARDS_RAW_DATA[self.slug][0]}"
    
    def setCardMove(self, move: 'MoveSchema'):
        self.card_move = C_Card_Move(**move.__dict__)
        print(f'Definindo card_move de {self.in_game_id}')
        print(self.card_move.__dict__)

    def reset(self):
        self.wisdom_cost = STANDARD_CARDS_RAW_DATA[self.slug][1]
        self.attack_point = STANDARD_CARDS_RAW_DATA[self.slug][2]
        self.defense_point = STANDARD_CARDS_RAW_DATA[self.slug][3]

        self.status: str = 'ready'

    def getStats(self):
        _data = {
            "slug": self.slug,
            "in_game_id": self.in_game_id,
            "card_type": self.card_type,
            "wisdom_cost": self.wisdom_cost,
            "status": self.status,
        }
        return _data

    # Movimentação

    async def onInvoke(self, match: 'C_Match'):
        self.player = match._getPlayerById(self.in_game_id.split("_")[0])
        if self.player.wisdom_available < self.wisdom_cost:
            return
        Logger.info(msg=f'O jogador {self.player.id} invocou a carta {
                    self.in_game_id}.', tag='C_Card_Match')
        self.player.card_hand.remove(self)
        self.player.card_prepare_camp.append(self)
        self.status = "used"
        self.can_move = False
        self.can_attack = False
        self.player.wisdom_available -= self.wisdom_cost

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        self.player = match._getPlayerById(self.in_game_id.split("_")[0])
        Logger.info(msg=f'O jogador {self.player.id} ressussitou a carta {
                    self.in_game_id}.', tag='C_Card_Match')

    async def onMoveToBattleZone(self, match: 'C_Match'):
        Logger.info(msg=f'O jogador {self.player.id} moveu a carta {
                    self.in_game_id} para Zona de Batalha.', tag='C_Card_Match')
        self.can_move = False
        self.can_attack = True
        self.player.card_prepare_camp.remove(self)
        self.player.card_battle_camp.append(self)

    async def onRetreatToPrepareZone(self, match: 'C_Match'):
        Logger.info(msg=f'O jogador {self.player.id} recuou a carta {
                    self.in_game_id} para Zona de Preparação.', tag='C_Card_Match')

    # Habilidades

    async def prepend(self, match: 'C_Match'):
        match.card_stack.addCard(self)
        await match.card_stack.notChange(match.move_now.player_move_id)
        for _team in match.players_in_match:
            for _player in _team:
                # if _player.id == match.move_now.player_move: continue
                notify = Notification(message=f"%PLAYER_NAME:{match.move_now.player_move_id}% adicionou o milagre {
                                      self} à lista.", title='Milagre', stillUntilDismiss=True)
                await match.sendToPlayer(data=notify.getData(),
                                         player_id=_player.id)

    async def addSkill(self, match: 'C_Match'):
        Logger.info(msg=f'O jogador {self.player.id} ativou habilidade da carta {
                    self.in_game_id}.', tag='C_Card_Match')

    async def rmvSkill(self, match: 'C_Match'):
        Logger.info(msg=f'A habilidade da carta {
                    self.in_game_id} foi removida.', tag='C_Card_Match')

    # Batalha

    async def onAttack(self, match: 'C_Match'):
        Logger.info(msg=f'O Jogador {self.player.id} está atacando com a carta {
                    self.in_game_id}.', tag='C_Card_Match')

    async def onDefense(self, match: 'C_Match'):
        Logger.info(msg=f'O Jogador {self.player.id} {
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
        Logger.info(msg=f'O Jogador {self.player.id} atacou o jogador {
                    player_target.id} com a carta {self.in_game_id}.', tag='C_Card_Match')

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
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, self.player.card_prepare_camp)
        self.player.card_prepare_camp.remove(self)
        card_target.attached_cards.append(self)
        Logger.info(msg=f'O artefato {self.in_game_id} foi equipado ao Herói {
                    card_target}.', tag='C_Card_Match')
        # Verificar a armadura de Deus

    async def onDettach(self, match: 'C_Match'):
        # self is hero card
        # card_target is the attached card to remove
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, self.attached_cards)
        self.attached_cards.remove(card_target)
        self.player.card_prepare_camp.append(card_target)
        Logger.info(msg=f'O artefato {self.in_game_id} foi removido do Herói {
                    card_target}.', tag='C_Card_Match')

# Utilitários


def getCardInListBySlugId(card_id: str, card_list: List[C_Card_Match]) -> C_Card_Match | None:
    '''
    Search in a list a card with the given ID
    '''
    if card_id != None:
        for card in card_list:
            if card != None:
                if card.in_game_id.find(card_id) >= 0:
                    return card
    return None


def getCardInListBySlug(card_slug: str, card_list: List[C_Card_Match]) -> C_Card_Match | None:
    '''
    Search in a list, an card with the given slug
    '''
    if card_slug != None:
        for card in card_list:
            if card != None:
                if card.slug == card_slug:
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
