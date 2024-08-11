from random import choice
from schemas.cards_schema import CardSchema,  MatchSchema, PlayersInMatchSchema, getCardInListBySlugId


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


Abraao = CardSchema(
    slug="abraao",
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    card_type="hero",
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
        if getCardInListBySlugId("eva", player.card_prepare_camp) or getCardInListBySlugId("eva", player.card_battle_camp):
            await self.addSkill()

    async def onDestroy(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onDestroy(player, match)
        self.resetCardStats()


Adao = C_Adao(
    slug="adao",
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type="hero",
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
    slug="daniel",
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    card_type="hero",
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
    slug="davi",
    wisdom_cost=3,
    attack_point=3,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)


class C_Elias(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        print(match.move_now)
        print(f"{match.move_now.card_id} destroi a carta {
              match.move_now.card_target}")
        player_target = match._getPlayerById(match.move_now.player_target)
        await match.moveCard(player_target, match.move_now.card_target, "battle", "forgotten")


Elias = C_Elias(
    slug="elias",
    wisdom_cost=4,
    attack_point=3,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)


class C_Ester(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        self.status = "ready"
        send_data = player.getPlayerStats(private=True)
        __card_deck = []
        for __card in player.card_deck[:3]:
            __card_deck.append(
                {
                    "slug": __card.slug,
                    "in_game_id": __card.in_game_id
                }
            )
        send_data["card_deck"] = __card_deck
        await match.sendToPlayer(
            data={
                "data_type": "player_update",
                "player_data": send_data
            },
            player_id=player.id
        )
        await super().onInvoke(player, match)
        self.status = "used"
        return True


Ester = C_Ester(
    slug="ester",
    wisdom_cost=1,
    attack_point=0,
    defense_points=2,
    card_type="hero",
    in_game_id=None,
)


class C_Eva(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        match.giveCard(player, 1)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId("adao", player.card_prepare_camp)
        if card:
            await card.addSkill()
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId("adao", player.card_battle_camp)
        if card:
            await card.addSkill()


Eva = C_Eva(
    slug="eva",
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)


Jaco = CardSchema(
    slug="jaco",
    wisdom_cost=2,
    attack_point=2,
    defense_points=2,
    card_type="hero",
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
    slug="jose-do-egito",
    wisdom_cost=2,
    attack_point=2,
    defense_points=1,
    card_type="hero",
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
    slug="josue",
    wisdom_cost=3,
    attack_point=3,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)


class C_Maria(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        self.status = "ready"
        send_data = player.getPlayerStats(private=True)
        __card_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'hero':
                __card_deck.append(
                    {
                        "slug": __card.slug,
                        "in_game_id": __card.in_game_id
                    }
                )
        print(send_data)
        print(__card_deck)
        send_data["card_deck"] = __card_deck
        await match.sendToPlayer(
            data={
                "data_type": "player_update",
                "player_data": send_data
            },
            player_id=player.id
        )
        await super().onInvoke(player, match)
        self.status = "used"
        return True


Maria = C_Maria(
    slug="maria",
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)


Moises = CardSchema(
    slug="moises",
    wisdom_cost=3,
    attack_point=2,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)


Noe = CardSchema(
    slug="noe",
    wisdom_cost=1,
    attack_point=2,
    defense_points=1,
    card_type="hero",
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
    slug="salomao",
    wisdom_cost=4,
    attack_point=2,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)


class C_Sansao(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        await match.moveCard(player, self.in_game_id, "prepare", "battle")
        self.status = "ready"


Sansao = C_Sansao(
    slug="sansao",
    wisdom_cost=6,
    attack_point=5,
    defense_points=5,
    card_type="hero",
    in_game_id=None
)
