from schemas import CardSchema

def getCardInListBySlug(card_slug: str, card_list: list[CardSchema]) -> CardSchema | None:
    for card in card_list:
        if card.card_slug == card_slug:
            return card
    return None