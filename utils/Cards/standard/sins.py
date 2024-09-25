import asyncio  # Usado por Diluvio
from typing import TYPE_CHECKING, List

from .base_cards import C_Card_Match, getCardInListBySlugId

from utils.console import consolePrint

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match


class C_Sins(C_Card_Match):

    def __init__(self, slug: str, in_game_id: str):
        super().__init__(slug, in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        await match.sendToPlayer(
            data={
                "data_type": "card_skill",
                "card_data": {
                    "slug": self.slug,
                }
            },
            player_id=player.id
        )
        

    async def addSkill(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().addSkill(match)
        player.card_prepare_camp.remove(self)
        player.card_in_forgotten_sea.append(self)
        self.reset()


class C_FrutoProibido(C_Sins):
    slug = 'fruto-proibido'
    fe_inabalavel = True
    incorruptivel = True

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Destroi o herói do oponente que esteja te atacando, se ele tem Adão e ou Eva na ZB, ambos são destruídos


class C_Idolatria(C_Sins):
    slug = 'idolatria'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        # Quando um herói te ataque ou defenda, destrua todos os artefatos aquipados a ele
        await super().addSkill(match)
        player_target = match._getPlayerById(match.move_now.player_target_id)
        card_target = getCardInListBySlugId(card_id=match.move_now.card_target_id, card_list=player_target.card_battle_camp)
        for _card in card_target.attached_cards:
            player_target.card_in_forgotten_sea.append(_card)
            _card.reset()



class C_Traicao(C_Sins):
    slug = 'traicao'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # O oponente que te esteja atacando não pode atacar neste turno. Se Sansão estava entre os heróis atacantes, destrua-o.
