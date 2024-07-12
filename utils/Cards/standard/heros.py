# from schemas.players_schema import PlayersInMatchSchema
# from schemas.matches_schema import MatchSchema
from schemas.cards_schema import CardSchema, ConfigDict

# from utils.Cards import getCardInListBySlug


Abraao = CardSchema(
    slug="abraao",
    wisdom_cost=2,
    attack_point=1,
    defense_points=2,
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

# def passiveSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     if self in player.card_battle_camp:
#         # Precisa de evento ao entrar herói no jogo
#         player.faith_points += 1

Adao = CardSchema(
    slug="adao",
    wisdom_cost=1,
    attack_point=1,
    defense_points=1,
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

#     # def passiveSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     if (getCardInListBySlug(slug='eva', card_list=player.card_battle_camp)) or (getCardInListBySlug(slug='eva', card_list=player.card_prepare_camp)):
#     #         # Verificar por EVA
#     #         self.attack_point += 2
#     #         self.defense_points += 2

Daniel = CardSchema(
    slug = "daniel",
    wisdom_cost = 2,
    attack_point = 1,
    defense_points = 2,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     oponents_in_target_battle_zone = player.card_battle_camp.__len__()
#     #     # Precisa manter até o fim do turno
#     #     self.attack_point += oponents_in_target_battle_zone

Davi = CardSchema(
        slug = "davi",
        wisdom_cost = 3,
        attack_point = 3,
        defense_points = 2,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     player.faith_points -= 1

Elias = CardSchema(
    slug = "elias",
    wisdom_cost = 4,
    attack_point = 3,
    defense_points = 1,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     oponent_target = player
#     #     # Precisa definir a carta a ser destuída
#     #     card_id = 0
#     #     oponent_target.card_battle_camp.remove(card_id)

Ester = CardSchema(
    slug = "ester",
    wisdom_cost = 1,
    attack_point = 0,
    defense_points = 2,
    in_game_id=None
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     # Precisa reorganizar
#     #     return player.card_deck[:3]

Eva = CardSchema(
    slug = "eva",
    wisdom_cost = 1,
    attack_point = 1,
    defense_points = 1,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     # Precisa verificar se está entrando no jogo
#     #     game.giveCard(player, 1)

Jaco = CardSchema(
    slug = "jaco",
    wisdom_cost = 2,
    attack_point = 2,
    defense_points = 2,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

JoseDoEgito = CardSchema(
    slug = "jose-do-egito",
    wisdom_cost = 2,
    attack_point = 2,
    defense_points = 1,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Josue = CardSchema(
    slug = "josue",
    wisdom_cost = 3,
    attack_point = 3,
    defense_points = 1,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Maria = CardSchema(
    slug = "maria",
    wisdom_cost = 2,
    attack_point = 1,
    defense_points = 2,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Moises = CardSchema(
    slug = "moises",
    wisdom_cost = 3,
    attack_point = 2,
    defense_points = 1,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Noe = CardSchema(
    slug = "noe",
    wisdom_cost = 1,
    attack_point = 2,
    defense_points = 1,
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

#     # def passiveSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     ...

Salomao = CardSchema(
    slug = "salomao",
    wisdom_cost = 4,
    attack_point = 2,
    defense_points = 2,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     self.used = True

Sansao = CardSchema(
    slug = "sansao",
    wisdom_cost = 6,
    attack_point = 5,
    defense_points = 5,
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

#     # def activeSkill(self, player: PlayersInMatchSchema, game: MatchSchema):
#     #     self.used = True
