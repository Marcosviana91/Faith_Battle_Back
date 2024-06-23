from random import choice

# Used in TinyDB and JSON schemas


class User:
    '''
    Dados de identificação do usuário para login
    '''

    def __init__(
        self,
        id: int | None,
        username: str | None,
        password: str | None,
        created_at: str | None,
        last_login: str | None,
        real_name: str | None,
        email: str | None,
    ) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.created_at = created_at
        self.last_login = last_login
        self.real_name = real_name
        self.email = email

# Salvo em Tiny DB


class Player:
    '''
    Dados do usuário, relativos ao jogo (como jogador)
    '''

    def __init__(
        self,
        id: int,
        xp_points: int = 0,
        available_cards: list[str] = []
    ):
        self.id = id
        self.xp_points = xp_points
        self.available_cards = [
            'abraao', 'adao', 'daniel',
            'davi', 'elias', 'ester',
            'eva', 'jaco', "jose-do-egito",
            "josue", "maria", "moises",
            "noe", "salomao", "sansao"
        ] if available_cards == [] else available_cards

    def onJoinMatch(self):
        ...

    def onEndMatch(self):
        ...


class Players_in_Match:
    def __init__(self, id: int, card_deck: list[str]):
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


class Card:
    def __init__(self, in_game_id: str):
        self.in_game_id = in_game_id
        # nome único: jose-do-egito
        self.card_slug: str
        # player id - card slug - secret
        self.in_game_id: str
        # hero, artifacts, miracles, sins, legendary, wisdom
        self.card_wisdom_cost: int
        self.card_attack_points: int
        self.card_defense_points: int
        self.card_has_passive_skill: bool
        self.card_has_active_skill: bool
        self.card_attachable: bool

        self.ready: bool

    def __str__(self):
        return f'\n########\n{self.card_slug}: {self.in_game_id}\n{self.card_wisdom_cost}, {self.card_attack_points}, {self.card_defense_points}\n########\n'

    def passiveSkill(self):
        ...

    def activeSkill(self):
        ...

    def onAttach(self):
        ...

    def onDettach(self):
        ...

    def onDestroy(self):
        ...

    def onInvoke(self):
        ...

    def onAttack(self):
        ...

    def onDefense(self):
        ...


class Move:
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


class RetryCards:
    player_id: int
    cards_id: list[int]


class GameData:
    def __init__(
        self,
        data_type: str,
        player: Players_in_Match | None = None,
        player_id: int | None = None,
        room_id: int | None = None,
        move: Move | None = None,
        retry_cards: RetryCards | None = None
    ):
        self.room_id = room_id
        self.data_type = data_type  # connect, change_deck, retry_cards, move
        self.player = player
        self.player_id = player_id
        self.move = move
        self.retry_cards = retry_cards


class GameRoomSchema:
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
        # print(__file__,f"\nGameRoomSchema.__init__\nPlayer {player_create_match.id} has create a room (ID: {self.id})")
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
    def __dict__(self):
        __players_in_match = []
        for player in self.players_in_match:
            _player = {
                "id": player.id,
                "ready": player.ready,
                "faith": player.faith_points,
                "wisdom": player.wisdom_points,
                "wisdom_used": player.wisdom_used,
                "cards_in_prepare_zone": player.card_prepare_camp,
                "cards_in_battle_zone": player.card_battle_camp,
                "cards_in_forgotten_sea": player.card_in_forgotten_sea
            }
            __players_in_match.append(_player)

        return {
            "id": self.id,
            "created_by": self.created_by,
            "room_name": self.room_name,
            "room_game_type": 'survival',
            "room_current_players": self.players_in_match.__len__(),
            "room_max_players": self.max_players,
            "has_password": (self.password != ""),
            "stage": self.game_stage,

            "players_in_match": __players_in_match
        }

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
            card_selected = choice(player.card_deck)
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


class APIResponseProps:
    def __init__(
        self,
        message: str | None,
    ):
        self.message = message
        self.data_type = 'error'
        self.user_data: dict = {}
        self.room_data: dict = {}
        self.room_list: list = []
        self.player_data: dict = {}
        # self.player_in_match_data: Players_in_Match = None
        # self.card_data: Card = None
        # self.game_data: GameData = None

    # @property
    # def __dict__(self):
    #     __temp = {
    #         "data_type": self.data_type,
    #         "user_data": self.user_data,
    #         "room_data": self.room_data,
    #         "player_data": self.player_data,
    #     }
    #     __reponse = {}

    #     for k, v in __temp.items():
    #         if v:
    #             __reponse[k] = v

    #     return __reponse


class ClientRequestProps:
    def __init__(
        self,
        **kwargs,
    ):
        # print(__file__,'\nClientRequestProps.__init__\n' ,kwargs)
        self.data_type: str = kwargs.get('data_type')
        self.user_data: dict = kwargs.get("user_data")  # User
        self.room_data: dict = kwargs.get("room_data")
        self.player_data: dict = kwargs.get("player_data")
        # self.player_in_match_data: dict = kwargs.get("player_in_match_data")
        # self.card_data: dict = kwargs.get("card_data")
        # self.game_data: dict = kwargs.get("game_data")

    @property
    def __dict__(self):
        __temp = {
            "data_type": self.data_type,
            "user_data": self.user_data,
            "room_data": self.room_data,
            "player_data": self.player_data,
        }
        __reponse = {}

        for k, v in __temp.items():
            if v:
                __reponse[k] = v

        return __reponse
