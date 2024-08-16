from random import choice
from schemas.cards_schema import CardSchema,  MatchSchema, PlayersInMatchSchema, getCardInListBySlugId

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

Abraao = CardSchema(
    slug='abraao',
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


class C_Adao(CardSchema):
    def resetCardStats(self):
        self.attack_point = 1,
        self.defense_points = 1

    async def addSkill(self):
        await super().addSkill()
        self.attack_point += 2
        self.defense_points += 2

    async def rmvSkill(self):
        await super().rmvSkill()
        self.attack_point -= 2
        self.defense_points -= 2

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Procurar por Eva no campo de preparação e no campo de batalha
        if getCardInListBySlugId('eva', player.card_prepare_camp) or getCardInListBySlugId('eva', player.card_battle_camp):
            await self.addSkill()

    async def onDestroy(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onDestroy(player, match)
        self.resetCardStats()


Adao = C_Adao(
    slug='adao',
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Daniel(CardSchema):

    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 1
        self.defense_points = 2

    async def rmvSkill(self):
        await super().rmvSkill()
        self.attack_point -= self.increase_attack
        self.increase_attack = 0

    async def onAttack(self, player: PlayersInMatchSchema, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().onAttack(player, attack_cards, player_target, match)
        print('Habilidade de Daniel')
        self.increase_attack = len(player_target.card_battle_camp)
        print(f'{self.increase_attack} cartas no campo de batalha do jogador {
              player_target.id}')
        self.attack_point += self.increase_attack


Daniel = C_Daniel(
    slug='daniel',
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


class C_Davi(CardSchema):
    async def onAttack(self, player: PlayersInMatchSchema, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().onAttack(player, attack_cards, player_target, match)
        print(f'Tirar um ponto de fé do jogador {self.skill_focus_player_id}')
        skill_player_target = match._getPlayerById(self.skill_focus_player_id)
        if skill_player_target is not None:
            match.takeDamage(skill_player_target, 1)


Davi = C_Davi(
    slug='davi',
    wisdom_cost=3,
    attack_point=3,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


class C_Elias(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                }
            },
            player_id=player.id
        )

    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)
        await match.moveCard(player_target, match.move_now.card_target, 'battle', 'forgotten')
        consolePrint.status(
            f'A carta {match.move_now.card_target} foi destruída')


Elias = C_Elias(
    slug='elias',
    wisdom_cost=4,
    attack_point=3,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Ester(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
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
        return False


Ester = C_Ester(
    slug='ester',
    wisdom_cost=1,
    attack_point=0,
    defense_points=2,
    card_type='hero',
    in_game_id=None,
)


class C_Eva(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        match.giveCard(player, 1)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId('adao', player.card_prepare_camp)
        if card:
            await card.addSkill()
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId('adao', player.card_battle_camp)
        if card:
            await card.addSkill()


Eva = C_Eva(
    slug='eva',
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Jaco(CardSchema):
    async def onAttack(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().onAttack(player, attack_cards, player_target, match)
        if len(player_target.card_hand) > 0:
            card_to_show = choice(player_target.card_hand)
            if card_to_show.card_type == 'miracle':
                match.giveCard(player, 1)
            await match.sendToPlayer(
                data={
                    'data_type': 'card_skill',
                    'card_data': {
                        'slug': self.slug,
                        'deck': [{'slug':card_to_show.slug, 'card_type': card_to_show.card_type}]
                    }
                },
                player_id=player.id
            )


Jaco = C_Jaco(
    slug='jaco',
    wisdom_cost=2,
    attack_point=2,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


class C_JoseDoEgito(CardSchema):
    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 2,
        self.defense_points = 1

    async def addSkill(
        self,
        player: PlayersInMatchSchema | None = None,
        attack_cards: list[CardSchema] | None = None,
        player_target: PlayersInMatchSchema | None = None,
        match: MatchSchema | None = None
    ):
        await super().addSkill()
        if len(player_target.card_hand) < 1:
            print('Não tem cartas para descartar')
        else:
            __card_to_discart = choice(player_target.card_hand)
            await match.moveCard(
                player=player_target,
                card_id=__card_to_discart.in_game_id,
                move_from='hand',
                move_to='forgotten'
            )
            print(f'Descartou a carta {
                  __card_to_discart.in_game_id} na sala {match.id}')

    async def rmvSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().rmvSkill()
        match.giveCard(player, 1)

    async def hasSuccessfullyAttacked(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, defense_cards: list[CardSchema] | None = None, match: MatchSchema | None = None):
        await super().hasSuccessfullyAttacked(player, attack_cards, player_target, defense_cards, match)
        await self.addSkill(player_target=player_target, match=match)

    async def hasNotSuccessfullyAttacked(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, defense_cards: list[CardSchema] | None = None, match: MatchSchema | None = None):
        await super().hasNotSuccessfullyAttacked(player, attack_cards, player_target, defense_cards, match)
        await self.rmvSkill(player=player, match=match)


JoseDoEgito = C_JoseDoEgito(
    slug='jose-do-egito',
    wisdom_cost=2,
    attack_point=2,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Josue(CardSchema):
    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 3
        self.defense_points = 1

    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill()
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Add 1/0 to {card.in_game_id}')
                card.attack_point += 1

    async def rmvSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().rmvSkill(player, attack_cards, player_target, match)
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Remove 1/0 to {card.in_game_id}')
                card.attack_point -= 1

    async def onAttack(self, player: PlayersInMatchSchema, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().onAttack(player, attack_cards, player_target, match)
        await self.addSkill(attack_cards=attack_cards)


Josue = C_Josue(
    slug='josue',
    wisdom_cost=3,
    attack_point=3,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Maria(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
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
    card_type='hero',
    in_game_id=None
)


class C_Moise(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
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

    async def addSkill(self, player: PlayersInMatchSchema | None = None, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().addSkill(player, attack_cards, player_target, match)
        card_id = match.move_now.card_list[0].in_game_id
        card_in_deck = getCardInListBySlugId(card_id, player.card_deck)
        card_in_sea = getCardInListBySlugId(
            card_id, player.card_in_forgotten_sea)
        print(card_in_deck, card_in_sea)
        if card_in_deck is not None:
            player.card_deck.remove(card_in_deck)
            player.card_hand.append(card_in_deck)
            card_in_deck.status = 'ready'
        elif card_in_sea is not None:
            player.card_in_forgotten_sea.remove(card_in_sea)
            player.card_hand.append(card_in_sea)
            card_in_sea.status = 'ready'


Moises = C_Moise(
    slug='moises',
    wisdom_cost=3,
    attack_point=2,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


Noe = CardSchema(
    slug='noe',
    wisdom_cost=1,
    attack_point=2,
    defense_points=1,
    card_type='hero',
    in_game_id=None
)


class C_Salomao(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        if player.wisdom_points < 10:
            player.wisdom_available += 1
            player.wisdom_points += 1

    async def onAttack(self, player: PlayersInMatchSchema, attack_cards: list[CardSchema] | None = None, player_target: PlayersInMatchSchema | None = None, match: MatchSchema | None = None):
        await super().onAttack(player, attack_cards, player_target, match)
        if player.wisdom_available < player.wisdom_points:
            player.wisdom_available += 1


Salomao = C_Salomao(
    slug='salomao',
    wisdom_cost=4,
    attack_point=2,
    defense_points=2,
    card_type='hero',
    in_game_id=None
)


class C_Sansao(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'


Sansao = C_Sansao(
    slug='sansao',
    wisdom_cost=6,
    attack_point=5,
    defense_points=5,
    card_type='hero',
    in_game_id=None
)
