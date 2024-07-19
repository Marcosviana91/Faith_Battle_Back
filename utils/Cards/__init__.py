from secrets import token_hex
from schemas.cards_schema import CardSchema
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


def createCardListObjectsByPlayer(player_id: int, card_list: list[CardSchema]) -> list[CardSchema]:
    card_object = []
    heroes: list[CardSchema] = STANDARD_HEROS_CLASSES['HEROS']
    for card in card_list:
        for hero in heroes:
            if card.slug == hero.slug:
                __temp_id = f'{player_id}-{card.slug}-{token_hex(3)}'
                newHero = hero.model_copy()
                newHero.in_game_id = __temp_id
                card_object.append(newHero)
                break
    return card_object

def cardListToDict(card_list:list[CardSchema]):
            __list = []
            for card in card_list:
                __list.append(card.getCardStats)
            return __list

# def getCardInListBySlug(card_slug: str, card_list: list[CardSchema]) -> CardSchema | None:
#     for card in card_list:
#         if card.slug == card_slug:
#             return card
#     return None
