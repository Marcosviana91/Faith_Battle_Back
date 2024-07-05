from secrets import token_hex

from schemas import Players_in_Match, Card

from .standard import heros

STANDARD_HEROS_CLASSES = {
    'HEROS': [
        heros.Abraao,
        heros.Adao,
        heros.Daniel,
        heros.Davi,
        heros.Elias,
        heros.Ester,
        heros.Eva,
        heros.Jaco,
        heros.JoseDoEgito,
        heros.Josue,
        heros.Maria,
        heros.Moises,
        heros.Noe,
        heros.Salomao,
        heros.Sansao
    ]
}

def createCardListObjectsByPlayer(player: Players_in_Match) -> list[Card]:
    card_object = []
    heroes: list[Card] = STANDARD_HEROS_CLASSES['HEROS']
    for card in player.card_deck:
        for hero in heroes:
            if card == hero.card_slug:
                __temp_id = f'{player.id}-{card}-{token_hex(3)}'
                newHero: Card = hero(__temp_id)
                card_object.append(newHero)
    return card_object
