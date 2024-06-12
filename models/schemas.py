from sqlmodel import SQLModel

# Used in TinyDB and JSON schemas
class Players_in_Match(SQLModel):
    id: int
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
    move_type: str # start, retry_cards, attack, defense, attach, dettach, active, passive
    player_target: int
    card_target: int | None
    
class RetryCards(SQLModel):
    player_id: int
    cards_id: list[int]

class GameData(SQLModel):
    data_type: str # connect, start, move, retry_cards
    room_id: int
    player: Players_in_Match | None
    move: Move | None
    retry_cards: RetryCards | None
    
    def __init__(self, data_type:str, player: Players_in_Match | None = None, move: Move | None = None, retry_cards: RetryCards | None = None):
        self.data_type = data_type
        self.player = player
        self.move = move
        self.retry_cards = retry_cards