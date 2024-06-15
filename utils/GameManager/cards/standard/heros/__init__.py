from models import Card
from models.schemas import Players_in_Match, GameRoomSchema


class Abraao(Card):
    card_slug = "abraao"

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        if self in player.card_battle_camp:
            # Precisa de evento ao entrar herói no jogo
            player.faith_points += 1


class Adao(Card):
    card_slug = "adao"

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        if ("eva" in player.card_battle_camp) or ("eva" in player.card_prepare_camp):
            # Precisa verificar por EVA
            self.card_attack_points += 2
            self.card_defense_points += 2


class Daniel(Card):
    card_slug = "daniel"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        oponents_in_target_battle_zone = player.card_battle_camp.__len__()
        # Precisa manter até o fim do turno
        self.card_attack_points += oponents_in_target_battle_zone


class Davi(Card):
    card_slug = "davi"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        player.faith_points -= 1


class Elias(Card):
    card_slug = "elias"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        oponent_target = player
        # Precisa definir a carta a ser destuída
        card_id = 0
        oponent_target.card_battle_camp.remove(card_id)


class Ester(Card):
    card_slug = "ester"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        # Precisa reorganizar
        return player.card_deck[:3]


class Eva(Card):
    card_slug = "eva"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        # Precisa verificar se está entrando no jogo
        game.giveCard(player, 1)


class Jaco(Card):
    card_slug = "jaco"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class JoseDoEgito(Card):
    card_slug = "jose-do-egito"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Josue(Card):
    card_slug = "josue"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Maria(Card):
    card_slug = "maria"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Moises(Card):
    card_slug = "moises"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Moises(Card):
    card_slug = "moises"

    def passiveSkill(self, player: Players_in_Match, game: GameRoomSchema):
        ...


class Salomao(Card):
    card_slug = "salomao"

    def activeSkill(self, player: Players_in_Match, game: GameRoomSchema):
        self.ready = True
