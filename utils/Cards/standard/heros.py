from random import choice
from schemas.cards_schema import CardSchema,  MatchSchema, PlayersInMatchSchema, getCardInListBySlugId

from utils.console import consolePrint
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA


STANDARD_CARDS_HEROS = [
    'abraao',
    'adao',
    'daniel',
    'davi',
    'elias',
    'ester',
    'eva',
    'jaco',
    'jose-do-egito',
    'josue',
    'maria',
    'moises',
    'noe',
    'salomao',
    'sansao',
]


class Heros(CardSchema):
    attached_cards: list[CardSchema] = []
    card_type: str = 'hero'

    def getCardStats(self):
        data = super().getCardStats()
        _attached_cards = []
        for card in self.attached_cards:
            _attached_cards.append(card.getCardStats())
        data["attached_cards"] = _attached_cards
        return data

    async def onAttack(self, match: MatchSchema | None = None):
        await super().onAttack(match)
        # A passiva da Botas do Evangelho é verificada para todos os heróis
        if getCardInListBySlugId('botas-do-evangelho', self.attached_cards):
            player = match._getPlayerById(match.move_now.player_move)
            new_card = match.giveCard(player)
            if new_card:
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": 'Botas do Evangelho',
                        "message": f'Comprou a carta {new_card.slug}.',
                        "stillUntilDismiss": True
                    }
                }, player_id=player.id)
        # A passiva do Cinturao da Verdade é verificada para todos os heróis
        if getCardInListBySlugId('cinturao-da-verdade', self.attached_cards):
            player = match._getPlayerById(match.move_now.player_move)
            player_target = match._getPlayerById(match.move_now.player_target)
            if len(player_target.card_deck) > 0:
                reveled_card = player_target.card_deck[0]
                reveled_card_wisdom_cost = STANDARD_CARDS_RAW_DATA[reveled_card.slug][1]
                consolePrint.info(f'Jogador {player_target.id} revelou a carta {
                                  STANDARD_CARDS_RAW_DATA[reveled_card.slug][0]}')
                match.takeDamage(player_target, reveled_card_wisdom_cost)
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Cinturão da Verdade",
                        "message": f'Jogador {player_target.id} revelou a carta {STANDARD_CARDS_RAW_DATA[reveled_card.slug][0]} com {reveled_card_wisdom_cost} de custo.',
                        'stillUntilDismiss': True
                    }
                }, player_id=player.id)
            else:
                consolePrint.info('Não há carta para revelar')

    async def onInvoke(self, match: MatchSchema | None = None):
        await super().onInvoke(match)
        player = match._getPlayerById(match.move_now.player_move)
        # A passiva de Abraão é verificada para todos os heróis
        if getCardInListBySlugId('abraao', player.card_battle_camp):
            consolePrint.info(f'CARD: {player.id} ativou abraão')
            player.faith_points += 1

    async def onMoveToAttackZone(self, match: MatchSchema | None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onMoveToAttackZone(match)
        # A passiva de Arca da Aliança é verificada para todos os heróis
        if getCardInListBySlugId('arca-da-alianca', player.card_battle_camp):
            consolePrint.info(f'CARD: {player.id} ativou Arca da Aliança')
            self.attack_point += 1
            self.defense_points += 1

    async def onRetreatToPrepareZone(self, match: MatchSchema | None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onRetreatToPrepareZone(match)
        # A passiva de Arca da Aliança é verificada para todos os heróis
        if getCardInListBySlugId('arca-da-alianca', player.card_battle_camp):
            consolePrint.info(
                f'CARD: {player.id} removeu o efeito Arca da Aliança')
            self.attack_point -= 1
            self.defense_points -= 1


class C_Abraao(Heros):
    ...


Abraao = C_Abraao(
    slug='abraao',
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    in_game_id=None,
)


class C_Adao(Heros):
    def resetCardStats(self):
        self.attack_point = 1,
        self.defense_points = 1

    async def addSkill(self, match: MatchSchema | None = None):
        await super().addSkill(match)
        self.attack_point += 2
        self.defense_points += 2

    async def rmvSkill(self, match: MatchSchema | None = None):
        await super().rmvSkill(match)
        self.attack_point -= 2
        self.defense_points -= 2

    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        # Procurar por Eva no campo de preparação e no campo de batalha
        if getCardInListBySlugId('eva', player.card_prepare_camp) or getCardInListBySlugId('eva', player.card_battle_camp):
            await self.addSkill(match)

    async def onDestroy(self, match: MatchSchema | None = None):
        await super().onDestroy(match)
        self.resetCardStats()


Adao = C_Adao(
    slug='adao',
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    in_game_id=None
)


class C_Daniel(Heros):

    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 1
        self.defense_points = 2

    async def rmvSkill(self, match: MatchSchema | None = None):
        await super().rmvSkill(match)
        self.attack_point -= self.increase_attack
        self.increase_attack = 0

    async def onAttack(self, match: MatchSchema | None = None):
        player_target = match._getPlayerById(match.move_now.player_target)
        await super().onAttack(match)
        self.increase_attack = len(player_target.card_battle_camp)
        self.attack_point += self.increase_attack


Daniel = C_Daniel(
    slug='daniel',
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    in_game_id=None
)


class C_Davi(Heros):
    async def onAttack(self, match: MatchSchema | None = None):
        await super().onAttack(match)
        print(f'Tirar um ponto de fé do jogador {self.skill_focus_player_id}')
        await match.sendToPlayer(
            data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Davi",
                    "message": "Você perdeu um ponto de fé",
                    'stillUntilDismiss': True
                }},
            player_id=self.skill_focus_player_id
        )
        skill_player_target = match._getPlayerById(self.skill_focus_player_id)
        if skill_player_target is not None:
            match.takeDamage(skill_player_target, 1)


Davi = C_Davi(
    slug='davi',
    wisdom_cost=3,
    attack_point=3,
    defense_points=2,
    in_game_id=None
)


class C_Elias(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                }
            },
            player_id=player.id
        )
        for _player in match.players_in_match:
            # if _player.id == match.move_now.player_move: continue
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Elias",
                    "message": f"Elias está orando..."
                }
            }, player_id=_player.id)

    async def addSkill(self, match: MatchSchema | None = None):
        await super().addSkill(match)
        if not match.move_now.player_target:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Elias",
                    "message": f"Faltou sabedoria..."
                }
            }, player_id=match.move_now.player_move)
        else:
            player_target = match._getPlayerById(match.move_now.player_target)
            await match.moveCard(player_target, match.move_now.card_target, 'battle', 'forgotten')
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Elias",
                    "message": f"Sua carta foi destruída: {match.move_now.card_target.split('_')[1]}"
                }
            }, player_id=player_target.id)
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "2 Reis 1:12",
                    "message": f"Respondeu Elias: Se sou homem de Deus, que desça fogo do céu e consuma você e seus cinquenta soldados!... De novo fogo de Deus desceu e consumiu o oficial e seus soldados.",
                    "stillUntilDismiss": True
                }
            }, player_id=player_target.id)


Elias = C_Elias(
    slug='elias',
    wisdom_cost=4,
    attack_point=3,
    defense_points=1,
    in_game_id=None
)


class C_Ester(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        __card_deck = []
        for __card in player.card_deck[:3]:
            __card_deck.append(
                {
                    'slug': __card.slug,
                    'in_game_id': __card.in_game_id
                }
            )
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': __card_deck
                }
            },
            player_id=player.id
        )


Ester = C_Ester(
    slug='ester',
    wisdom_cost=1,
    attack_point=0,
    defense_points=2,
    in_game_id=None,
)


class C_Eva(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        match.giveCard(player, 1)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId('adao', player.card_prepare_camp)
        if card:
            await card.addSkill(match)
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId('adao', player.card_battle_camp)
        if card:
            await card.addSkill(match)


Eva = C_Eva(
    slug='eva',
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    in_game_id=None
)


class C_Jaco(Heros):
    async def onAttack(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        player_target = match._getPlayerById(match.move_now.player_target)
        await super().onAttack(match)
        if len(player_target.card_hand) > 0:
            card_to_show = choice(player_target.card_hand)
            if card_to_show.card_type == 'miracle':
                match.giveCard(player, 1)
            await match.sendToPlayer(
                data={
                    'data_type': 'card_skill',
                    'card_data': {
                        'slug': self.slug,
                        'deck': [{'slug': card_to_show.slug, 'card_type': card_to_show.card_type}]
                    }
                },
                player_id=player.id
            )


Jaco = C_Jaco(
    slug='jaco',
    wisdom_cost=2,
    attack_point=2,
    defense_points=2,
    in_game_id=None
)


class C_JoseDoEgito(Heros):
    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 2,
        self.defense_points = 1

    async def addSkill(self, match: MatchSchema | None = None):
        player_target = match.fight_camp.player_defense
        await super().addSkill(match)
        if len(player_target.card_hand) < 1:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"O oponente não tem cartas para descartar."
                }
            }, player_id=match.fight_camp.player_attack)
        else:
            __card_to_discart = choice(player_target.card_hand)
            await match.moveCard(
                player=player_target,
                card_id=__card_to_discart.in_game_id,
                move_from='hand',
                move_to='forgotten'
            )
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"A carta {__card_to_discart.in_game_id} foi descartada."
                }
            }, player_id=match.fight_camp.player_attack)
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"A carta {__card_to_discart.in_game_id} foi descartada."
                }
            }, player_id=match.fight_camp.player_defense)

    async def rmvSkill(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().rmvSkill(match)
        gived_card: CardSchema = match.giveCard(player, 1)
        if gived_card:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f'Você comprou a carta {gived_card.slug}.'
                }
            }, player_id=match.fight_camp.player_attack)
        else:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"Não foi possível comprar uma carta."
                }
            }, player_id=match.fight_camp.player_attack)

    async def hasSuccessfullyAttacked(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, defense_cards: list[CardSchema] | None = None, match: MatchSchema | None = None):
        await super().hasSuccessfullyAttacked(player, attack_cards, player_target, defense_cards, match)
        await self.addSkill(match=match)

    async def hasNotSuccessfullyAttacked(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, defense_cards: list[CardSchema] | None = None, match: MatchSchema | None = None):
        await super().hasNotSuccessfullyAttacked(player, attack_cards, player_target, defense_cards, match)
        await self.rmvSkill(match=match)


JoseDoEgito = C_JoseDoEgito(
    slug='jose-do-egito',
    wisdom_cost=2,
    attack_point=2,
    defense_points=1,
    in_game_id=None
)


class C_Josue(Heros):
    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 3
        self.defense_points = 1

    async def addSkill(self, match: MatchSchema | None = None):
        attack_cards = match.fight_camp.attack_cards
        await super().addSkill(match)
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Add 1/0 to {card.in_game_id}')
                card.attack_point += 1

    async def rmvSkill(self, match: MatchSchema | None = None):
        attack_cards = match.fight_camp.attack_cards
        await super().rmvSkill(match)
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Remove 1/0 to {card.in_game_id}')
                card.attack_point -= 1

    async def onAttack(self, match: MatchSchema | None = None):
        await super().onAttack(match)
        await self.addSkill(match)


Josue = C_Josue(
    slug='josue',
    wisdom_cost=3,
    attack_point=3,
    defense_points=1,
    in_game_id=None
)


class C_Maria(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        __heros_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'hero':
                __heros_in_deck.append(
                    {
                        'slug': __card.slug,
                        'in_game_id': __card.in_game_id
                    }
                )
        sorted_cards = sorted(__heros_in_deck, key=lambda card: card['slug'])
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_cards
                }
            },
            player_id=player.id
        )


Maria = C_Maria(
    slug='maria',
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    in_game_id=None
)


class C_Moise(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        __miracles_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'miracle':
                __miracles_in_deck.append(
                    {
                        'slug': __card.slug,
                        'in_game_id': __card.in_game_id
                    }
                )
        sorted_miracles_in_deck = sorted(
            __miracles_in_deck, key=lambda card: card['slug'])

        __miracles_in_forgoten_sea = []
        for __card_forgotten in player.card_in_forgotten_sea:
            if __card_forgotten.card_type == 'miracle':
                __miracles_in_forgoten_sea.append(
                    {
                        'slug': __card_forgotten.slug,
                        'in_game_id': __card_forgotten.in_game_id
                    }
                )
        sorted_miracles_in_forgoten_sea = sorted(
            __miracles_in_forgoten_sea, key=lambda card: card['slug'])
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_miracles_in_deck,
                    'forgotten_sea': sorted_miracles_in_forgoten_sea,
                }
            },
            player_id=player.id
        )

    async def addSkill(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().addSkill(match)
        card_id = match.move_now.card_list[0].in_game_id
        card_in_deck = getCardInListBySlugId(card_id, player.card_deck)
        card_in_sea = getCardInListBySlugId(
            card_id, player.card_in_forgotten_sea)
        print(card_in_deck, card_in_sea)
        if card_in_deck is not None:
            player.card_deck.remove(card_in_deck)
            player.card_hand.append(card_in_deck)
            card_in_deck.status = 'ready'
            for _player in match.players_in_match:
                if _player.id == player.id:
                    continue
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Habilidade de Moisés",
                        "message": f"Moisés antecipou a carta {card_in_deck.slug}."
                    }
                }, player_id=_player.id)
        elif card_in_sea is not None:
            player.card_in_forgotten_sea.remove(card_in_sea)
            player.card_hand.append(card_in_sea)
            card_in_sea.status = 'ready'
            for _player in match.players_in_match:
                if _player.id == player.id:
                    continue
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Habilidade de Moisés",
                        "message": f"Moisés resgatou a carta {card_in_sea.slug}."
                    }
                }, player_id=_player.id)


Moises = C_Moise(
    slug='moises',
    wisdom_cost=3,
    attack_point=2,
    defense_points=2,
    in_game_id=None
)


class C_Noe(Heros):
    ...


Noe = C_Noe(
    slug='noe',
    wisdom_cost=1,
    attack_point=2,
    defense_points=1,
    in_game_id=None
)


class C_Salomao(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        if player.wisdom_points < 10:
            player.wisdom_available += 1
            player.wisdom_points += 1
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Salomão",
                    "message": f"Você ganhou 1 ponto de sabedoria."
                }
            }, player_id=player.id)

    async def onAttack(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onAttack(match)
        if player.wisdom_available < player.wisdom_points:
            player.wisdom_available += 1


Salomao = C_Salomao(
    slug='salomao',
    wisdom_cost=4,
    attack_point=2,
    defense_points=2,
    in_game_id=None
)


class C_Sansao(Heros):
    async def onInvoke(self, match: MatchSchema | None = None):
        player = match._getPlayerById(match.move_now.player_move)
        await super().onInvoke(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Habilidade de Sansão",
                "message": f"Sansão está pronto para atacar."
            }
        }, player_id=player.id)


Sansao = C_Sansao(
    slug='sansao',
    wisdom_cost=6,
    attack_point=5,
    defense_points=5,
    in_game_id=None
)
