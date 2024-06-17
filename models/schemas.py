# Used in TinyDB and JSON schemas


class Players_in_Match:
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

    def __str__(self):
        return self.id

    @property
    def getInfo(self):
        return [
            self.id,
            self.ready,
            self.card_deck,
            self.card_hand,
            self.card_prepare_camp,
            self.card_battle_camp,
            self.card_in_forgotten_sea,
            self.faith_points,
            self.wisdom_points,
            self.wisdom_used,
        ]


class Move():
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


class RetryCards():
    player_id: int
    cards_id: list[int]


class GameData():
    def __init__(
        self,
        data_type: str,
        player: Players_in_Match | None = None,
        player_id: int | None = None,
        move: Move | None = None,
        retry_cards: RetryCards | None = None
    ):
        room_id: int
        self.data_type = data_type  # connect, change_deck, retry_cards, move
        self.player = player
        self.player_id = player_id
        self.move = move
        self.retry_cards = retry_cards


class GameRoomSchema():
    '''
    #### Stages
        0: players has connecteds, check decks
        1: sort cards to all players, retry sort
        2: game in curse
    game_stage: int
    '''
    # Stages
    #   0: players has connecteds, check decks
    #   1: sort cards to all players, retry sort
    #   2: game in curse

    def __init__(self, player_create_match: Players_in_Match, room_name: str, max_players: int, match_type: str, password: str):
        self.id = id(self)
        print(
            f"Player {player_create_match.id} has create a room (ID: {self.id})")
        self.players_in_match: list[Players_in_Match] = []
        self.room_name = room_name
        self.created_by = player_create_match.id
        self.max_players = max_players
        self.match_type = match_type
        self.password = password

        self.start_match = ''
        self.game_stage = 0
        self.round = 0
        self.player_turn = 0
        self.player_focus_id = None
        self.can_others_moves = False
        self.end_match = ''

    @property
    def getInfo(self):
        return [
            self.id,
            self.room_name,
            self.created_by,
            self.getPlayersIdList(),
            self.max_players,
            self.match_type,
            self.password,
            self.game_stage,
            self.round,
            self.player_turn,
            self.can_others_moves,
            self.player_focus_id
        ]

    def getPlayerByPlayerId(self, player_id: int) -> Players_in_Match:
        for player in self.players_in_match:
            if player.id == player_id:
                return player
        raise IndexError(f'Player with id {player_id} not found')

    def getPlayersIdList(self):
        __players_info = []
        for player in self.players_in_match:
            __players_info.append(player.id)
        return __players_info

    def getPlayersInfo(self):
        ...

    def allPlayersIsReady(self) -> bool:
        count = 0
        for player in self.players_in_match:
            if player.ready == True:
                count += 1
        if count == len(self.players_in_match):
            self.game_stage += 1
            self.setPlayersNotReady()
            print(f"All players is ready.\nNext stage: stage {
                  self.game_stage}")
            return True
        return False

    def setPlayersNotReady(self):
        for player in self.players_in_match:
            player.ready = False

    def giveCard(self, player: Players_in_Match, number_of_cards: int = 1):
        # print(f"Sorteando {number_of_cards} cartas para o jogador {player.id}...")
        count = 0
        while count < number_of_cards:
            card_selected = player.card_deck[0]
            # card_selected = choice(player.card_deck)
            player.card_hand.append(card_selected)
            count += 1
            player.card_deck.remove(card_selected)
        # print(f"mão: {player.card_hand}\ndeck: {player.card_deck}")

    def gameHandle(self, data: GameData):
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
