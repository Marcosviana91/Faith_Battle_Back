# from secrets import token_hex
# from schemas.cards_schema import CardSchema


# def createCardListObjectsByPlayer(player_id: int, card_list: list[str]) -> list[CardSchema]:
#     card_object = []
#     heroes: list[CardSchema] = STANDARD_HEROS_CLASSES['HEROS']
#     for card in card_list:
#         for hero in heroes:
#             if card == hero.slug:
#                 __temp_id = f'{player_id}-{card}-{token_hex(3)}'
#                 newHero: CardSchema = hero(__temp_id)
#                 card_object.append(newHero)
#     print(card_object)
#     return card_object
