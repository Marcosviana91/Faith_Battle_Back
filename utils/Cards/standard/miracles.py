import asyncio  # Usado por Diluvio
from schemas.cards_schema import CardSchema, MatchSchema, PlayersInMatchSchema, getCardInListBySlugId

from utils.console import consolePrint


class MoveSchema:
    match_id: str
    round_match: int
    player_move: int
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive, done
    card_id: str | None = None
    player_target: int | None = None
    card_target: str | None = None
    card_list: list[CardSchema] | None = []

##################################################################


STANDARD_CARDS_MIRACLES = [
    # 'cordeiro-de-deus',
    'diluvio',
    'fogo-do-ceu',
    # 'forca-de-sansao',
    # 'liberacao-celestial',
    # 'no-ceu-tem-pao',
    # 'passagem-segura',
    # 'protecao-divina',
    # 'ressurreicao',
    'restauracao-de-fe',
    'sabedoria-de-salomao',
    'sarca-ardente',
]


class C_CordeiroDeDeus(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Até seu próximo turno, o jogador alvo não perde pontos de fé, pecados não o afetam e suas cartas são indestritívies


CordeiroDeDeus = C_CordeiroDeDeus(
    slug='cordeiro-de-deus',
    wisdom_cost=4,
    card_type='miracle',
    in_game_id=None,
)


class C_Diluvio(CardSchema):

    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Destrói todos os heróis e artefatos da zona de batalha. Noé e a Arca sobrevivem
        # Verificar Arca de Noé dentre as cartas acopladas aos heróis - FALTA
        _card_list_whitout_noe = list(
            filter(lambda _card: _card.slug != 'noe', player_target.card_battle_camp))
        tasks = [await match.moveCard(player=player_target, card_id=_card.in_game_id,
                                      move_from='battle', move_to='forgotten') for _card in _card_list_whitout_noe]
        try:
            await asyncio.wait(tasks)
        except AttributeError as e:
            consolePrint.danger(f'MIRACLE: AttributeError {e}')


Diluvio = C_Diluvio(
    slug='diluvio',
    wisdom_cost=6,
    card_type='miracle',
    in_game_id=None,
)


class C_FogoDoCeu(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Destrói uma carta da zona de batalha
        # Mesma habilidade de Elias
        await match.moveCard(player_target, match.move_now.card_target, 'battle', 'forgotten')
        consolePrint.status(
            f'A carta {match.move_now.card_target} foi destruída')


FogoDoCeu = C_FogoDoCeu(
    slug='fogo-do-ceu',
    wisdom_cost=3,
    card_type='miracle',
    in_game_id=None,
)


class C_ForcaDeSansao(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # O herói alvo ganha 3/3 até o final do turno. Se o alvo é Sansão, ele se torna indestrutível até o final do turno.


ForcaDeSansao = C_ForcaDeSansao(
    slug='forca-de-sansao',
    wisdom_cost=2,
    card_type='miracle',
    in_game_id=None,
)


class C_LiberacaoCelestial(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Anula qualquer efeito de milagre ou pecado nesse instante.


LiberacaoCelestial = C_LiberacaoCelestial(
    slug='liberacao-celestial',
    wisdom_cost=2,
    card_type='miracle',
    in_game_id=None,
)


class C_NoCeuTemPao(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # O jogador alvo compra 3 cartas, se voce tem moisés em sua zona de batalha, compre 5.


NoCeuTemPao = C_NoCeuTemPao(
    slug='no-ceu-tem-pao',
    wisdom_cost=3,
    card_type='miracle',
    in_game_id=None,
)


class C_PassagemSegura(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Os heróis do jogador alvo são imbloqueáveis neste turno


PassagemSegura = C_PassagemSegura(
    slug='passagem-segura',
    wisdom_cost=4,
    card_type='miracle',
    in_game_id=None,
)


class C_ProtecaoDivina(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # O jogador alvo não sofre dano de efeitos ou ataque de Heróis neste turno


ProtecaoDivina = C_ProtecaoDivina(
    slug='protecao-divina',
    wisdom_cost=1,
    card_type='miracle',
    in_game_id=None,
)


class C_Ressurreicao(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # Retorna um herói de qualquer mar do esquecimento ao jogo sob seu controle. Voce escolhe em qual zona ele voltará.


Ressurreicao = C_Ressurreicao(
    slug='ressurreicao',
    wisdom_cost=3,
    card_type='miracle',
    in_game_id=None,
)


class C_RestauracaoDeFe(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # O jogador alvo ganha um ponto de fé por cada herói no campo de batlaha dele.
        faith_count = 0
        for _card in player_target.card_battle_camp:
            if _card.card_type == 'hero':
                faith_count += 1
        player_target.faith_points += faith_count
        consolePrint.info(f'O jogador {player_target.id} ganhou {
                          faith_count} pontos de fé.')


RestauracaoDeFe = C_RestauracaoDeFe(
    slug='restauracao-de-fe',
    wisdom_cost=2,
    card_type='miracle',
    in_game_id=None,
)


class C_SabedoriaDeSalomao(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, match)
        # O jogador alvo reativa 3 cartas de sabedoria.
        player_target.wisdom_available += 3
        if player_target.wisdom_available > player_target.wisdom_points:
            player_target.wisdom_available = player_target.wisdom_points
        # Se Salomão está em jogo, compre uma carta.
        salomao_in_prepare = getCardInListBySlugId(
            'salomao', player_target.card_prepare_camp)
        salomao_in_battle = getCardInListBySlugId(
            'salomao', player_target.card_battle_camp)
        if salomao_in_battle or salomao_in_prepare:
            consolePrint.info('MIRACLE: Compra 1 carta')
            match.giveCard(player=player_target)


SabedoriaDeSalomao = C_SabedoriaDeSalomao(
    slug='sabedoria-de-salomao',
    wisdom_cost=1,
    card_type='miracle',
    in_game_id=None,
)


class C_SarcaArdente(CardSchema):
    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list['CardSchema'] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        player_target2: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None,
    ):
        await super().addSkill(player, attack_cards, player_target, player_target2, match)
        # O jogador alva ganha 2 pontos de fé e o oponente alvo perde 2 pontos de fé
        player_target.faith_points +=2
        match.takeDamage(player_target2, 2)


SarcaArdente = C_SarcaArdente(
    slug='sarca-ardente',
    wisdom_cost=2,
    card_type='miracle',
    in_game_id=None,
)
