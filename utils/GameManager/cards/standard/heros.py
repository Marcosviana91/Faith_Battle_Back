from models import Card
from models.schemas import Players_in_Match, GameRoomSchema

from utils.GameManager.cards.utils import getCardInListBySlug


class Abraao(Card):
    card_type = 1
    card_slug = "abraao"
    card_name = "Abraão"
    card_wisdom_cost = 2
    card_attack_points = 1
    card_defense_points = 2
    card_has_passive_skill = True
    card_has_active_skill = False
    card_attachable = False
    ready = False

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        if self in player.card_battle_camp:
            # Precisa de evento ao entrar herói no jogo
            player.faith_points += 1


class Adao(Card):
    card_type = 1
    card_slug = "adao"
    card_name = "Adão"
    card_wisdom_cost = 1
    card_attack_points = 1
    card_defense_points = 1
    card_has_passive_skill = True
    card_has_active_skill = False
    card_attachable = False

    ready = False

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        if (getCardInListBySlug(card_slug='eva', card_list=player.card_battle_camp)) or (getCardInListBySlug(card_slug='eva', card_list=player.card_prepare_camp)):
            # Verificar por EVA
            self.card_attack_points += 2
            self.card_defense_points += 2


class Daniel(Card):
    card_slug = "daniel"
    card_type = 1
    card_name = "Daniel"
    card_wisdom_cost = 2
    card_attack_points = 1
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        oponents_in_target_battle_zone = player.card_battle_camp.__len__()
        # Precisa manter até o fim do turno
        self.card_attack_points += oponents_in_target_battle_zone


class Davi(Card):
    card_slug = "davi"
    card_type = 1
    card_name = 'Davi'
    card_wisdom_cost = 3
    card_attack_points = 3
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        player.faith_points -= 1


class Elias(Card):
    card_slug = "elias"
    card_type = 1
    card_name = 'Elias'
    card_wisdom_cost = 4
    card_attack_points = 3
    card_defense_points = 1
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        oponent_target = player
        # Precisa definir a carta a ser destuída
        card_id = 0
        oponent_target.card_battle_camp.remove(card_id)


class Ester(Card):
    card_slug = "ester"
    card_type = 1
    card_name = 'Ester'
    card_wisdom_cost = 1
    card_attack_points = 0
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        # Precisa reorganizar
        return player.card_deck[:3]


class Eva(Card):
    card_slug = "eva"
    card_type = 1
    card_name = 'Eva'
    card_wisdom_cost = 1
    card_attack_points = 1
    card_defense_points = 1
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        # Precisa verificar se está entrando no jogo
        game.giveCard(player, 1)


class Jaco(Card):
    card_slug = "jaco"
    card_type = 1
    card_name = 'Jacó'
    card_wisdom_cost = 2
    card_attack_points = 2
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class JoseDoEgito(Card):
    card_slug = "jose-do-egito"
    card_type = 1
    card_name = 'José do Egito'
    card_wisdom_cost = 2
    card_attack_points = 2
    card_defense_points = 1
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Josue(Card):
    card_slug = "josue"
    card_type = 1
    card_name = 'Josué'
    card_wisdom_cost = 3
    card_attack_points = 3
    card_defense_points = 1
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Maria(Card):
    card_slug = "maria"
    card_type = 1
    card_name = 'Maria'
    card_wisdom_cost = 2
    card_attack_points = 1
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Moises(Card):
    card_slug = "moises"
    card_type = 1
    card_name = 'Moisés'
    card_wisdom_cost = 3
    card_attack_points = 2
    card_defense_points = 1
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Noe(Card):
    card_slug = "noe"
    card_type = 1
    card_name = 'Noé'
    card_wisdom_cost = 1
    card_attack_points = 2
    card_defense_points = 1
    card_has_passive_skill = True
    card_has_active_skill = False
    card_attachable = False

    ready = False

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Salomao(Card):
    card_slug = "salomao"
    card_type = 1
    card_name = 'Salomão'
    card_wisdom_cost = 4
    card_attack_points = 2
    card_defense_points = 2
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    ready = False

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        self.ready = True


class Sansao(Card):
    card_slug = "sansao"
    card_type = 1
    card_name = 'Sansão'
    card_wisdom_cost = 6
    card_attack_points = 5
    card_defense_points = 5
    card_has_passive_skill = False
    card_has_active_skill = True
    card_attachable = False

    # Sansão entra em jogo pronto para atacar
    ready = True

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        self.ready = True
