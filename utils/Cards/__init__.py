from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from utils.ROOM.RoomClass import C_Card
    from utils.Cards.standard.base_cards import C_Card_Match

from .standard import heros, miracles, artifacts


STANDARD_CARDS_CLASSES: list['C_Card_Match'] = [
    heros.C_Abraao,
    heros.C_Adao,
    heros.C_Daniel,
    heros.C_Davi,
    heros.C_Elias,
    heros.C_Ester,
    heros.C_Eva,
    heros.C_Jaco,
    heros.C_JoseDoEgito,
    heros.C_Josue,
    heros.C_Maria,
    heros.C_Moises,
    heros.C_Noe,
    heros.C_Salomao,
    heros.C_Sansao,
    # miracles.C_CordeiroDeDeus,
    miracles.C_Diluvio,
    miracles.C_FogoDoCeu,
    # miracles.C_ForcaDeSansao,
    # miracles.C_LiberacaoCelestial,
    miracles.C_NoCeuTemPao,
    # miracles.C_PassagemSegura,
    # miracles.C_ProtecaoDivina,
    # miracles.C_Ressurreicao,
    miracles.C_RestauracaoDeFe,
    miracles.C_SabedoriaDeSalomao,
    miracles.C_SarcaArdente,
    artifacts.C_ArcaDaAlianca,
    # artifacts.C_ArcaDeNoe,
    artifacts.C_BotasDoEvangelho,
    artifacts.C_CajadoDeMoises,
    artifacts.C_CapaceteDaSalvacao,
    artifacts.C_CinturaoDaVerdade,
    artifacts.C_CouracaDaJustica,
    artifacts.C_EscudoDaFe,
    artifacts.C_EspadaDoEspirito,
    artifacts.C_Os10Mandamentos,
]


def createCardMatchByCardList(card_list: list['C_Card']) -> list['C_Card_Match']:
    card_object = []
    for card in card_list:
        for card_match in STANDARD_CARDS_CLASSES:
            if card.slug == card_match.slug:
                newCard = card_match(in_game_id=card.in_game_id)
                card_object.append(newCard)
                break
    return card_object


# def cardListToDict(card_list: list[CardSchema]):
#     __list = []
#     for card in card_list:
#         if card:
#             __list.append(card.getCardStats())
#         else:
#             __list.append({"slug": "not-defense"})
#     return __list
