from secrets import token_hex

from schemas.cards_schema import CardSchema

from .standard import heros, miracles

STANDARD_CARDS_CLASSES = [
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
        heros.Sansao,
        miracles.CordeiroDeDeus,
        miracles.Diluvio,
        miracles.FogoDoCeu,
        miracles.ForcaDeSansao,
        miracles.LiberacaoCelestial,
        miracles.NoCeuTemPao,
        miracles.PassagemSegura,
        miracles.ProtecaoDivina,
        miracles.Ressurreicao,
        miracles.RestauracaoDeFe,
        miracles.SabedoriaDeSalomao,
        miracles.SarcaArdente,
    ]



def createCardListObjectsByPlayer(player_id: int, card_list: list[CardSchema]) -> list[CardSchema]:
    card_object = []
    heroes: list[CardSchema] = STANDARD_CARDS_CLASSES
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
                if card:
                    __list.append(card.getCardStats)
                else:
                    __list.append({"slug": "not-defense"})
            return __list

def getCardInListBySlugId(card_slug: str, card_list: list[CardSchema]) -> CardSchema | None:
    if card_slug != None:
        for card in card_list:
            if card != None:
                if card.in_game_id.find(card_slug) >= 0:
                    return card
    return None
