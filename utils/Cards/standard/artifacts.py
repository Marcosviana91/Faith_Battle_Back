from typing import TYPE_CHECKING

from .base_cards import C_Card_Match, getCardInListBySlugId
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

from utils.console import consolePrint

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match


<<<<<<< HEAD
STANDARD_CARDS_ARTIFACTS = [
    'arca-da-alianca',
    # 'arca-de-noe',
    # 'botas-do-evangelho',
    # 'cajado-de-moises',
    # 'capacete-da-salvacao',
    # 'cinturao-da-verdade',
    # 'couraca-da-justica',
    # 'escudo-da-fe',
    # 'espada-do-espirito',
    'os-10-mandamentos',
]
=======
class C_Artifacts(C_Card_Match):

    def __init__(self, slug: str, in_game_id: str):
        super().__init__(slug, in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        self.status = 'ready'
>>>>>>> development


class C_ArcaDaAlianca(C_Artifacts):
    slug = 'arca-da-alianca'

    def __init__(self, in_game_id: str):
        super().__init__(slug='arca-da-alianca', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Todos os Heróis na ZB sob seu controle ganham 1/1. A Arca entra direto na ZB
        player = match._getPlayerById(match.move_now.player_move_id)
        for card in player.card_battle_camp:
            if card.card_type == "hero":
                card.attack_point += 1
                card.defense_point += 1
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Arca da Aliança",
                "message": f"Seus heróis ganham 1/1 no ZB."
            }
        }, player_id=player.id)

    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        player_target = match._getPlayerById(match.move_now.player_target_id)
        for card in player_target.card_battle_camp:
            if card.card_type == "hero":
                card.attack_point -= 1
                card.defense_point -= 1
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Arca da Aliança",
                "message": f"Sua arca foi destruída..."
            }
        }, player_id=player_target.id)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        await self.addSkill(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'

    async def onDestroy(self, match: 'C_Match'):
        await super().onDestroy(match)
        await self.rmvSkill(match)


class C_ArcaDeNoe(C_Artifacts):
    slug = 'arca-de-noe'

    def __init__(self, in_game_id: str):
        super().__init__(slug='arca-de-noe', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.indestrutivel = True
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Arca de Noé",
                "message": f"{card_target.slug} é indestrutível agora."
            }
        }, player_id=player.id)

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.indestrutivel = False


class C_BotasDoEvangelho(C_Artifacts):
    slug = 'botas-do-evangelho'

    # A passiva da Botas do Evangelho é verificada para todos os heróis na classe heros
    def __init__(self, in_game_id: str):
        super().__init__(slug='botas-do-evangelho', in_game_id=in_game_id)


class C_CajadoDeMoises(C_Artifacts):
    slug = 'cajado-de-moises'

    def __init__(self, in_game_id: str):
        super().__init__(slug='cajado-de-moises', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point += 1
        if card_target.slug == 'moises':
            for _card in [*player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]:
                if _card.card_type == "miracle":
                    if _card.wisdom_cost > 1:
                        _card.wisdom_cost -= 1
            consolePrint.status('O cajado foi equipado a Moisés')
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Moisés está com seu cajado",
                    "message": f"Seus milagres agora custam -1 de sabedoria."
                }
            }, player_id=player.id)

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point -= 1
        if card_target.slug == 'moises':
            consolePrint.status('O cajado foi removido de Moisés')
            all_cards = [*player.card_battle_camp, *player.card_prepare_camp,
                         *player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]
            for card in all_cards:
                card.wisdom_cost = STANDARD_CARDS_RAW_DATA[card.slug][1]
            card_os_10_mandamentos = getCardInListBySlugId(
                'os-10-mandamentos', player.card_battle_camp)
            if card_os_10_mandamentos:
                await card_os_10_mandamentos.addSkill(match)


class C_CapaceteDaSalvacao(C_Artifacts):
    slug = 'capacete-da-salvacao'

    def __init__(self, in_game_id: str):
        super().__init__(slug='capacete-da-salvacao', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point += 1
        card_target.incorruptivel = True
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Capacete da Salvação",
                "message": f"{card_target.slug} é incorruptível agora."
            }
        }, player_id=player.id)

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point -= 1
        card_target.incorruptivel = False


class C_CinturaoDaVerdade(C_Artifacts):
    slug = 'cinturao-da-verdade'

    def __init__(self, in_game_id: str):
        super().__init__(slug='cinturao-da-verdade', in_game_id=in_game_id)


class C_CouracaDaJustica(C_Artifacts):
    slug = 'couraca-da-justica'

    def __init__(self, in_game_id: str):
        super().__init__(slug='couraca-da-justica', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point += 2
        card_target.defense_point += 2

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point -= 2
        card_target.defense_point -= 2


class C_EscudoDaFe(C_Artifacts):
    slug = 'escudo-da-fe'

    def __init__(self, in_game_id: str):
        super().__init__(slug='escudo-da-fe', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.defense_point += 2

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.defense_point -= 2


class C_EspadaDoEspirito(C_Artifacts):
    slug = 'espada-do-espirito'

    def __init__(self, in_game_id: str):
        super().__init__(slug='espada-do-espirito', in_game_id=in_game_id)

    async def onAttach(self, match: 'C_Match'):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point += 1
        card_target.imbloqueavel = True
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Arca de Noé",
                "message": f"{card_target.slug} é imbloqueável agora."
            }
        }, player_id=player.id)

    async def onDettach(self, match: 'C_Match'):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card_target = getCardInListBySlugId(
            match.move_now.card_target_id, player.card_prepare_camp)
        card_target.attack_point -= 1
        card_target.imbloqueavel = False


class C_Os10Mandamentos(C_Artifacts):
    slug = 'os-10-mandamentos'

    def __init__(self, in_game_id: str):
        super().__init__(slug='os-10-mandamentos', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Suas cartas custam -1 de sabedoria para serem jogadas, não pode ser reduzido a 0
        player = match._getPlayerById(match.move_now.player_move_id)
        all_cards = [*player.card_battle_camp, *player.card_prepare_camp,
                     *player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]
        for card in all_cards:
            if card.wisdom_cost > 1:
                card.wisdom_cost -= 1
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Arca de Noé",
                "message": f"Suas cartas agora custam -1 de sabedoria."
            }
        }, player_id=player.id)

    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        # player = match._getPlayerById(match.move_now.player_move_id)
        player_target_id = int(self.in_game_id.split("_")[0])
        player_target = match._getPlayerById(player_target_id)
        all_cards = [*player_target.card_battle_camp, *player_target.card_prepare_camp,
                     *player_target.card_hand, *player_target.card_deck, *player_target.card_in_forgotten_sea]
        for card in all_cards:
            card.wisdom_cost = STANDARD_CARDS_RAW_DATA[card.slug][1]

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        await self.addSkill(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'

    async def onDestroy(self, match: 'C_Match'):
        await super().onDestroy(match)
        await self.rmvSkill(match)
