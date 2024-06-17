from models import Card

def getCardInListBySlug(card_slug: str, card_list: list[Card]) -> Card | None:
    for card in card_list:
        if card.card_slug ==card_slug:
            return card
    return None