from schemas.cards_schema import CardSchema, MatchSchema, PlayersInMatchSchema, getCardInListBySlugId


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


class C_CordeiroDeDeus(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Até seu próximo turno, o jogador alvo não perde pontos de fé, pecados não o afetam e suas cartas são indestritívies


CordeiroDeDeus = C_CordeiroDeDeus(
    slug="cordeiro-de-deus",
    wisdom_cost=4,
    card_type="miracle",
    in_game_id=None,
)


class C_Diluvio(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Destrói todos os heróis e artefatos da zona de batalha. Noé e a Arca sobrevivem


Diluvio = C_Diluvio(
    slug="diluvio",
    wisdom_cost=6,
    card_type="miracle",
    in_game_id=None,
)


class C_FogoDoCeu(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Destroi uma carta da zona de batalha


FogoDoCeu = C_FogoDoCeu(
    slug="fogo-do-ceu",
    wisdom_cost=3,
    card_type="miracle",
    in_game_id=None,
)


class C_ForcaDeSansao(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # O herói alvo ganha 3/3 até o final do turno. Se o alvo é Sansão, ele se torna indestrutível até o final do turno.


ForcaDeSansao = C_ForcaDeSansao(
    slug="forca-de-sansao",
    wisdom_cost=2,
    card_type="miracle",
    in_game_id=None,
)


class C_LiberacaoCelestial(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Anula qualquer efeito de milagre ou pecado nesse instante.


LiberacaoCelestial = C_LiberacaoCelestial(
    slug="liberacao-celestial",
    wisdom_cost=2,
    card_type="miracle",
    in_game_id=None,
)


class C_NoCeuTemPao(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # O jogador alvo compra 3 cartas, se voce tem moisés em sua zona de batalha, compre 5.


NoCeuTemPao = C_NoCeuTemPao(
    slug="no-ceu-tem-pao",
    wisdom_cost=3,
    card_type="miracle",
    in_game_id=None,
)


class C_PassagemSegura(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Os heróis do jogador alvo são imbloqueáveis neste turno


PassagemSegura = C_PassagemSegura(
    slug="passagem-segura",
    wisdom_cost=4,
    card_type="miracle",
    in_game_id=None,
)


class C_ProtecaoDivina(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # O jogador alvo não sofre dano de efeitos ou ataque de Heróis neste turno


ProtecaoDivina = C_ProtecaoDivina(
    slug="protecao-divina",
    wisdom_cost=1,
    card_type="miracle",
    in_game_id=None,
)


class C_Ressurreicao(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Retorna um herói de qualquer mar do esquecimento ao jogo sob seu controle. Voce escolhe em qual zona ele voltará.


Ressurreicao = C_Ressurreicao(
    slug="ressurreicao",
    wisdom_cost=3,
    card_type="miracle",
    in_game_id=None,
)


class C_RestauracaoDeFe(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # O jogador alvo não sofre dano de efeitos ou ataque de Heróis neste turno


RestauracaoDeFe = C_RestauracaoDeFe(
    slug="restauracao-de-fe",
    wisdom_cost=2,
    card_type="miracle",
    in_game_id=None,
)


class C_SabedoriaDeSalomao(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # O jogador alvo não sofre dano de efeitos ou ataque de Heróis neste turno


SabedoriaDeSalomao = C_SabedoriaDeSalomao(
    slug="sabedoria-de-salomao",
    wisdom_cost=1,
    card_type="miracle",
    in_game_id=None,
)


class C_SarcaArdente(CardSchema):
    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)


SarcaArdente = C_SarcaArdente(
    slug="sarca-ardente",
    wisdom_cost=2,
    card_type="miracle",
    in_game_id=None,
)
