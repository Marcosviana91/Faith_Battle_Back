from sqlmodel import SQLModel

# Used in TinyDB and JSON schemas

class Players_in_Match(SQLModel):
    id: int
    ready: bool
    card_deck: list
    deck_try: int
    card_hand: list
    card_in_forgotten_sea: list
    card_prepare_camp: list
    card_battle_camp: list
    faith_points: int
    wisdom_points: int
    wisdom_used: int

    def __init__(self, id, card_deck):
        self.id = id
        self.card_deck = card_deck
        self.ready = False
        self.deck_try = 0
        self.card_hand = []
        self.card_in_forgotten_sea = []
        self.card_prepare_camp = []
        self.card_battle_camp = []
        self.faith_points = 0
        self.wisdom_points = 0
        self.wisdom_used = 0


class Move(SQLModel):
    match_room_id: int
    match_round: int
    player_move: int
    card_id: int
    move_type: str  # move_to_prepare, move_to_battle, attack, defense, attach, dettach, active, passive
    player_target: int | None
    card_target: int | None

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


class RetryCards(SQLModel):
    player_id: int
    cards_id: list[int]


class GameData(SQLModel):
    data_type: str  # connect, change_deck, retry_cards, move
    room_id: int
    player: Players_in_Match | None
    player_id: int | None
    move: Move | None
    retry_cards: RetryCards | None

    def __init__(
        self,
        data_type: str,
        player: Players_in_Match | None = None,
        player_id: int | None = None,
        move: Move | None = None,
        retry_cards: RetryCards | None = None
    ):
        self.data_type = data_type
        self.player = player
        self.player_id = player_id
        self.move = move
        self.retry_cards = retry_cards


class GameRoomSchema:
    '''
    @ Property
    id: int
    start_match: str
    end_match: str

    #### Stages
        0: players has connecteds, check decks
        1: sort cards to all players, retry sort
        2: game in curse
    game_stage: int

    players_in_match: list[Players_in_Match] = []
    round: int
    moves = []

    player_turn: int  # index of player in player list
    player_focus: int | None

    '''
    id: int
    start_match: str
    end_match: str

    # Stages
    #   0: players has connecteds, check decks
    #   1: sort cards to all players, retry sort
    #   2: game in curse
    game_stage: int

    players_in_match: list[Players_in_Match] = []
    round: int
    moves = []

    player_turn: int  # index of player in player list
    can_others_moves: bool
    player_focus: int | None

    def getPlayerByPlayerId(self, player_id: int) -> Players_in_Match:
        ...

    def allPlayersIsReady(self) -> bool:
        ...

    def setPlayersNotReady(self):
        ...

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        '''
        Give to player a number of cards
        @ Params:
            player : Players_in_Match
            number_of_cards : int = 1
        @ Return None
        '''
        ...

    def gameStart() -> None:
        ...

    def newRoundHandle():
        '''
        Gives 1 wisdom for all player
        '''
        ...

    def playerTurnHandle():
        '''
        Sets used wisdom to 0 for current player
        and gives 1 card from deck
        '''
        ...
