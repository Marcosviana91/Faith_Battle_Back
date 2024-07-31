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

#     self.slug = "abraao"
#     self.wisdom_cost = 2
#     self.attack_point = 1
#     self.defense_points = 2
#     card_type = 1
#     has_passive_skill = True
#     has_active_skill = False
#     attachable = False
#     used = False

# def addSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     if self in player.card_battle_camp:
#         # Precisa de evento ao entrar herói no jogo
#         player.faith_points += 1


class C_Adao(CardSchema):
    def resetCardStats(self):
        self.attack_point = 1,
        self.defense_points = 1

    def addSkill(self):
        super().addSkill()
        self.attack_point += 2
        self.defense_points += 2

    def rmvSkill(self):
        super().rmvSkill()
        self.attack_point -= 2
        self.defense_points -= 2

    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        # Procurar por Eva no campo de preparação e no campo de batalha
        if getCardInListBySlugId("eva", player.card_prepare_camp) or getCardInListBySlugId("eva", player.card_battle_camp):
            self.addSkill()

    def onDestroy(self, player: PlayersInMatchSchema, match: MatchSchema):
        super().onDestroy(player, match)
        self.resetCardStats()


Adao = C_Adao(
    slug="adao",
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class Adao(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "adao"
#         self.wisdom_cost = 1
#         self.attack_point = 1
#         self.defense_points = 1
#     card_type = 1
#     card_name = "Adão"
#     has_passive_skill = True
#     has_active_skill = False
#     attachable = False

#     used = False

#     # def addSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     if (getCardInListBySlug(slug='eva', card_list=player.card_battle_camp)) or (getCardInListBySlug(slug='eva', card_list=player.card_prepare_camp)):
#     #         # Verificar por EVA
#     #         self.attack_point += 2
#     #         self.defense_points += 2


class C_Daniel(CardSchema):

    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 1
        self.defense_points = 2

    def rmvSkill(self):
        super().rmvSkill()
        self.attack_point -= self.increase_attack
        self.increase_attack = 0

    def onAttack(self, player: PlayersInMatchSchema, match: MatchSchema, player_target: PlayersInMatchSchema | None = None):
        super().onAttack(player, match, player_target)
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
# class Daniel(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "daniel"
#         self.wisdom_cost = 2
#         self.attack_point = 1
#         self.defense_points = 2
#     card_type = 1
#     card_name = "Daniel"
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     oponents_in_target_battle_zone = player.card_battle_camp.__len__()
#     #     # Precisa manter até o fim do turno
#     #     self.attack_point += oponents_in_target_battle_zone

Davi = CardSchema(
    slug="davi",
    wisdom_cost=3,
    attack_point=3,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)
# class Davi(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "davi"
#         self.wisdom_cost = 3
#         self.attack_point = 3
#         self.defense_points = 2
#     card_type = 1
#     card_name = 'Davi'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     player.faith_points -= 1


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
# class Elias(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "elias"
#         self.wisdom_cost = 4
#         self.attack_point = 3
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'Elias'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     oponent_target = player
#     #     # Precisa definir a carta a ser destuída
#     #     card_id = 0
#     #     oponent_target.card_battle_camp.remove(card_id)


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

# class Ester(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "ester"
#         self.wisdom_cost = 1
#         self.attack_point = 0
#         self.defense_points = 2
#     card_type = 1
#     card_name = 'Ester'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     # Precisa reorganizar
#     #     return player.card_deck[:3]


class C_Eva(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        match.giveCard(player, 1)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId("adao", player.card_prepare_camp)
        if card:
            card.addSkill()
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId("adao", player.card_battle_camp)
        if card:
            card.addSkill()


Eva = C_Eva(
    slug="eva",
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class Eva(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "eva"
#         self.wisdom_cost = 1
#         self.attack_point = 1
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'Eva'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     # Precisa verificar se está entrando no jogo
#     #     game.giveCard(player, 1)

Jaco = CardSchema(
    slug="jaco",
    wisdom_cost=2,
    attack_point=2,
    defense_points=2,
    card_type="hero",
    in_game_id=None
)
# class Jaco(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "jaco"
#         self.wisdom_cost = 2
#         self.attack_point = 2
#         self.defense_points = 2
#     card_type = 1
#     card_name = 'Jacó'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

JoseDoEgito = CardSchema(
    slug="jose-do-egito",
    wisdom_cost=2,
    attack_point=2,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class JoseDoEgito(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "jose-do-egito"
#         self.wisdom_cost = 2
#         self.attack_point = 2
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'José do Egito'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...


class C_Josue(CardSchema):
    def resetCardStats(self):
        super().resetCardStats()
        self.attack_point = 3
        self.defense_points = 1


Josue = C_Josue(
    slug="josue",
    wisdom_cost=3,
    attack_point=3,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class Josue(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "josue"
#         self.wisdom_cost = 3
#         self.attack_point = 3
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'Josué'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...


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
# class Maria(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "maria"
#         self.wisdom_cost = 2
#         self.attack_point = 1
#         self.defense_points = 2
#     card_type = 1
#     card_name = 'Maria'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Moises = CardSchema(
    slug="moises",
    wisdom_cost=3,
    attack_point=2,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class Moises(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "moises"
#         self.wisdom_cost = 3
#         self.attack_point = 2
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'Moisés'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Noe = CardSchema(
    slug="noe",
    wisdom_cost=1,
    attack_point=2,
    defense_points=1,
    card_type="hero",
    in_game_id=None
)
# class Noe(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "noe"
#         self.wisdom_cost = 1
#         self.attack_point = 2
#         self.defense_points = 1
#     card_type = 1
#     card_name = 'Noé'
#     has_passive_skill = True
#     has_active_skill = False
#     attachable = False

#     used = False

#     # def addSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...


class C_Salomao(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        if player.wisdom_points < 10:
            player.wisdom_available += 1
            player.wisdom_points += 1

    def onAttack(self, player: PlayersInMatchSchema, match: MatchSchema, player_target: PlayersInMatchSchema | None = None):
        super().onAttack(player, match, player_target)
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
# class Salomao(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "salomao"
#         self.wisdom_cost = 4
#         self.attack_point = 2
#         self.defense_points = 2
#     card_type = 1
#     card_name = 'Salomão'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     used = False

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     self.used = True


class C_Sansao(CardSchema):
    async def onInvoke(self, player: PlayersInMatchSchema, match: MatchSchema):
        await super().onInvoke(player, match)
        await match.moveCard(player, self.in_game_id, "prepare", "battle")
        self.status = "ready"
        print(player.id)
        print(match.id)


Sansao = C_Sansao(
    slug="sansao",
    wisdom_cost=6,
    attack_point=5,
    defense_points=5,
    card_type="hero",
    in_game_id=None
)


# class Sansao(CardSchema):
#     __pydantic_post_init__ = 'model_post_init'

#     def model_post_init(self, *args, **kwargs):
#         self.slug = "sansao"
#         self.wisdom_cost = 6
#         self.attack_point = 5
#         self.defense_points = 5
#     card_type = 1
#     card_name = 'Sansão'
#     has_passive_skill = False
#     has_active_skill = True
#     attachable = False

#     # Sansão entra em jogo pronto para atacar
#     used = True

#     # def rmvSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     self.used = True
