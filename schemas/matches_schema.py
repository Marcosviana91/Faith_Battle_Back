from datetime import datetime
from random import choice, shuffle

from pydantic import BaseModel

from schemas.games_schema import RoomSchema
from schemas.players_schema import PlayersInMatchSchema
from utils.Cards import createCardListObjectsByPlayer


MINIMUM_DECK_CARDS = 10
INITIAL_CARDS = 5
MAXIMUM_FAITH_POINTS = 15


class MoveSchema:
    match_room_id: int
    match_round: int
    player_move: int
    card_id: str
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive
    player_target: int | None
    card_target: str | None

    def __init__(
        self,
        player_move: int,
        card_id: int,
        move_type: str,
        player_target: int | None = None,
        card_target: int | None = None
    ):
        self.player_move = player_move
        self.card_id = card_id
        self.move_type = move_type
        self.player_target = player_target
        self.card_target = card_target


class MatchSchema(BaseModel):
    room: RoomSchema

    id: str = None
    start_match: str = None
    match_type: str = None
    players_in_match: list[PlayersInMatchSchema] = []
    round_match: int = 0
    player_turn: int = 0
    player_focus_id: int = 0
    can_others_move: bool = False
    end_match: str = None

    __pydantic_post_init__ = 'model_post_init'

    def model_post_init(self, *args, **kwargs):
        self.start_match = str(datetime.now().isoformat())
        self.id = self.room.id
        self.match_type = self.room.match_type
        for player in self.room.connected_players:
            new_player = PlayersInMatchSchema(
                id=player.id,
                card_deck=createCardListObjectsByPlayer(
                    player.id, player.card_deck),
                card_hand=createCardListObjectsByPlayer(
                    player.id, player.card_hand),
                faith_points=MAXIMUM_FAITH_POINTS
            )
            self.players_in_match.append(new_player)
        shuffle(self.players_in_match)
        del self.room
        self.newRoundHandle()

    @property
    def getMatchStats(self):
        __players_in_match = []
        for player in self.players_in_match:
            __players_in_match.append(player.getPlayerStats)

        return {
            "id": self.id,
            "start_match": self.start_match,
            "match_type": self.match_type,
            "round_match": self.round_match,
            "player_turn": self.player_turn,
            "player_focus_id": self.player_focus_id,
            "can_others_move": self.can_others_move,
            "players_in_match": __players_in_match,
        }

    def newRoundHandle(self):
        self.round_match += 1
        for player in self.players_in_match:
            if player.wisdom_points < 10:
                player.wisdom_points += 1
        self.player_turn = 0
        self.playerTurnHandle()

    def playerTurnHandle(self):
        print(f'Player {self.players_in_match[self.player_turn].id} turn:')
        player = self.players_in_match[self.player_turn]
        player.wisdom_used = 0
        self.giveCard(player)
        # O jogador prepara suas jogadas

    def giveCard(self, player: PlayersInMatchSchema, number_of_cards: int = 1):
        count = 0
        while count < number_of_cards:
            card_selected = player.card_deck[0]
            # card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)

    # Precisa gerar as cartas independentes
    def moveCard(self, player_id: int, card_id: str, move_from: str, move_to: str):
        print(f"Player {player_id} is moving the card {
              card_id}: {move_from} => {move_to}")

    def finishTurn(self):
        ...
