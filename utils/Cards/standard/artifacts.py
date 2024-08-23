from schemas.cards_schema import CardSchema, MatchSchema, getCardInListBySlugId

from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

from utils.console import consolePrint


class MoveSchema:
    match_id: str
    round_match: int
    player_move: int
    move_type: str  # move_to_prepare, move_to_battle, retreat_to_prepare, attack, defense, attach, dettach, active, passive, done, fight, surrender, change_deck, card_skill
    card_id: str | None = None
    player_target: int | None = None
    card_target: str | None = None
    card_list: list[CardSchema] | None = []

##################################################################


STANDARD_CARDS_ARTIFACTS = [
    'arca-da-alianca',
    'arca-de-noe',
    'botas-do-evangelho',
    'cajado-de-moises',
    'capacete-da-salvacao',
    'cinturao-da-verdade',
    'couraca-da-justica',
    'escudo-da-fe',
    'espada-do-espirito',
    'os-10-mandamentos',
]


class C_ArcaDaAlianca(CardSchema):
    async def addSkill(self, match: MatchSchema | None = None):
        await super().addSkill(match)
        # Todos os Heróis na ZB sob seu controle ganham 1/1. A Arca entra direto na ZB
        player = match._getPlayerById(match.move_now.player_move)
        for card in player.card_battle_camp:
            if card.card_type == "hero":
                card.attack_point += 1
                card.defense_points += 1

    async def rmvSkill(self, match: MatchSchema | None = None):
        await super().rmvSkill(match)
        player = match._getPlayerById(match.move_now.player_target)
        for card in player.card_battle_camp:
            if card.card_type == "hero":
                card.attack_point -= 1
                card.defense_points -= 1
        for _player in match.players_in_match:
            # if _player.id == player.id: continue
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Arca da Aliança",
                    "message": f"Sua arca foi destruída..."
                }
            }, player_id=_player.id)

    async def onInvoke(self, match: MatchSchema | None = None):
        await super().onInvoke(match)
        player = match._getPlayerById(match.move_now.player_move)
        await self.addSkill(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'

    async def onDestroy(self, match: MatchSchema | None = None):
        await super().onDestroy(match)
        await self.rmvSkill(match)


ArcaDaAlianca = C_ArcaDaAlianca(
    slug='arca-da-alianca',
    wisdom_cost=5,
    card_type='artifact',
    in_game_id=None,
)


class C_ArcaDeNoe(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.indestrutivel = True

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.indestrutivel = False


ArcaDeNoe = C_ArcaDeNoe(
    slug='arca-de-noe',
    wisdom_cost=5,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_BotasDoEvangelho(CardSchema):
    # A passiva da Botas do Evangelho é verificada para todos os heróis na classe heros
    ...


BotasDoEvangelho = C_BotasDoEvangelho(
    slug='botas-do-evangelho',
    wisdom_cost=2,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_CajadoDeMoises(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attack_point += 1
        if card_target.slug == 'moises':
            consolePrint.status('O cajado foi equipado a Moisés')
            for _card in [*player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]:
                if _card.card_type == "miracle":
                    if _card.wisdom_cost > 1:
                        _card.wisdom_cost -= 1

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
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


CajadoDeMoises = C_CajadoDeMoises(
    slug='cajado-de-moises',
    wisdom_cost=2,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_CapaceteDaSalvacao(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attack_point += 1
        card_target.incorruptivel = True

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attack_point -= 1
        card_target.incorruptivel = False


CapaceteDaSalvacao = C_CapaceteDaSalvacao(
    slug='capacete-da-salvacao',
    wisdom_cost=1,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_CinturaoDaVerdade(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)


CinturaoDaVerdade = C_CinturaoDaVerdade(
    slug='cinturao-da-verdade',
    wisdom_cost=4,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_CouracaDaJustica(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attack_point += 2
        card_target.defense_points += 2

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.attack_point -= 2
        card_target.defense_points -= 2


CouracaDaJustica = C_CouracaDaJustica(
    slug='couraca-da-justica',
    wisdom_cost=3,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_EscudoDaFe(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.defense_points += 2

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.defense_points -= 2

EscudoDaFe = C_EscudoDaFe(
    slug='escudo-da-fe',
    wisdom_cost=1,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_EspadaDoEspirito(CardSchema):
    async def onAttach(self, match: MatchSchema | None = None):
        await super().onAttach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.imbloqueavel = True

    async def onDettach(self, match: MatchSchema | None = None):
        await super().onDettach(match)
        player = match._getPlayerById(match.move_now.player_move)
        card_target = getCardInListBySlugId(
            match.move_now.card_target, player.card_prepare_camp)
        card_target.imbloqueavel = False


EspadaDoEspirito = C_EspadaDoEspirito(
    slug='espada-do-espirito',
    wisdom_cost=3,
    card_type='artifact',
    attachable=True,
    in_game_id=None,
)


class C_Os10Mandamentos(CardSchema):
    async def addSkill(self, match: MatchSchema | None = None):
        await super().addSkill(match)
        # Suas cartas custam -1 de sabedoria para serem jogadas, não pode ser reduzido a 0
        player = match._getPlayerById(match.move_now.player_move)
        all_cards = [*player.card_battle_camp, *player.card_prepare_camp,
                     *player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]
        for card in all_cards:
            if card.wisdom_cost > 1:
                card.wisdom_cost -= 1

    async def rmvSkill(self, match: MatchSchema | None = None):
        await super().rmvSkill(match)
        player = match._getPlayerById(match.move_now.player_move)
        all_cards = [*player.card_battle_camp, *player.card_prepare_camp,
                     *player.card_hand, *player.card_deck, *player.card_in_forgotten_sea]
        for card in all_cards:
            card.wisdom_cost = STANDARD_CARDS_RAW_DATA[card.slug][1]

    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        await self.addSkill(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'

    async def onDestroy(self, match: MatchSchema | None = None):
        await super().onDestroy(match)
        await self.rmvSkill(match)


Os10Mandamentos = C_Os10Mandamentos(
    slug='os-10-mandamentos',
    wisdom_cost=6,
    card_type='artifact',
    in_game_id=None,
)
