from random import choice
from typing import TYPE_CHECKING

from utils.console import consolePrint
from utils.LoggerManager import Logger
from .base_cards import C_Card_Match, getCardInListBySlugId

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match, C_Player_Match


class C_Heros(C_Card_Match):

    def __init__(self, slug: str, in_game_id: str):
        super().__init__(slug, in_game_id)

    def getStats(self):
        _data = super().getStats()
        _attached_cards = []
        for card in self.attached_cards:
            # recalcular o status da carta?
            _attached_cards.append(card.getStats())
        _attached_effects = []
        for card in self.attached_effects:
            # recalcular o status da carta?
            _attached_effects.append(card.getStats())
        _data.update({
            "attack_point": self.attack_point,
            "defense_point": self.defense_point,
            "attached_cards": _attached_cards,
            "attached_effects": _attached_effects,
            "imbloqueavel": self.imbloqueavel,
            "indestrutivel": self.indestrutivel,
            "incorruptivel": self.incorruptivel,
            "can_attack": self.can_attack,
            "can_move": self.can_move,
        })
        return _data

    async def onAttack(self, match: 'C_Match'):
        await super().onAttack(match)
        # A passiva da Botas do Evangelho é verificada para todos os heróis
        botas_do_evangelho = getCardInListBySlugId(
            'botas-do-evangelho', self.attached_cards)
        if botas_do_evangelho:
            await botas_do_evangelho.addSkill(match=match)

        # A passiva do Cinturao da Verdade é verificada para todos os heróis
        cinturao_da_verdade = getCardInListBySlugId(
            'cinturao-da-verdade', self.attached_cards)
        if cinturao_da_verdade:
            await cinturao_da_verdade.addSkill(match=match)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        # A passiva de Abraão é verificada para todos os heróis
        if getCardInListBySlugId('abraao', self.player.card_battle_camp):
            consolePrint.info(f'CARD: {self.player.id} ativou abraão')
            self.player.faith_points += 1
            self.player.fe_recebida += 1

    async def onMoveToBattleZone(self, match: 'C_Match'):
        await super().onMoveToBattleZone(match)
        # Seta os artefatos como 'used' para não poderem ser desequipados
        for _card in self.attached_cards:
            _card.status = 'used'
        # A passiva de Arca da Aliança é verificada para todos os heróis
        if getCardInListBySlugId('arca-da-alianca', self.player.card_battle_camp):
            consolePrint.info(f'CARD: {self.player.id} ativou Arca da Aliança')
            self.attack_point += 1
            self.defense_point += 1

    async def onRetreatToPrepareZone(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onRetreatToPrepareZone(match)
        # Seta os artefatos como 'ready' para poderem ser desequipados
        for _card in self.attached_cards:
            _card.status = 'ready'
        # A passiva de Arca da Aliança é verificada para todos os heróis
        if getCardInListBySlugId('arca-da-alianca', player.card_battle_camp):
            consolePrint.info(
                f'CARD: {player.id} removeu o efeito Arca da Aliança')
            self.attack_point -= 1
            self.defense_point -= 1

    async def onDestroy(self, match: 'C_Match'):
        player_target_id = int(self.in_game_id.split("_")[0])
        player_target = match._getPlayerById(player_target_id)
        await super().onDestroy(match)
        for _card in self.attached_cards:
            Logger.info(msg=f'O equipamento {
                        _card.in_game_id} foi destruída.', tag='C_Card_Match')
            player_target.card_in_forgotten_sea.append(_card)
        self.attached_cards = []


class C_Abraao(C_Heros):
    slug = 'abraao'

    def __init__(self, in_game_id: str):
        super().__init__(slug='abraao', in_game_id=in_game_id)


class C_Adao(C_Heros):
    slug = 'adao'

    def __init__(self, in_game_id: str):
        super().__init__(slug="adao", in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        self.attack_point += 2
        self.defense_point += 2

    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        self.attack_point -= 2
        self.defense_point -= 2

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        # Procurar por Eva no campo de preparação e no campo de batalha
        if getCardInListBySlugId('eva', self.player.card_prepare_camp) or getCardInListBySlugId('eva', self.player.card_battle_camp):
            Logger.info(msg='Adão encontrou Eva no jogo.', tag='C_Card_Match')
            await self.addSkill(match)

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        if getCardInListBySlugId('eva', player.card_prepare_camp) or getCardInListBySlugId('eva', player.card_battle_camp):
            Logger.info(msg='Adão encontrou Eva no jogo.', tag='C_Card_Match')
            self.addSkill(match)


class C_Daniel(C_Heros):
    slug = 'daniel'

    def __init__(self, in_game_id: str):
        super().__init__(slug="daniel", in_game_id=in_game_id)

    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        self.attack_point -= self.increase_attack
        self.increase_attack = 0

    async def onAttack(self, match: 'C_Match'):
        player_target = match._getPlayerById(match.move_now.player_target_id)
        await super().onAttack(match)
        self.increase_attack = len(player_target.card_battle_camp)
        self.attack_point += self.increase_attack


class C_Davi(C_Heros):
    slug = 'davi'

    def __init__(self, in_game_id: str):
        super().__init__(slug="davi", in_game_id=in_game_id)

    async def onAttack(self, match: 'C_Match'):
        await super().onAttack(match)
        print(f'Tirar um ponto de fé do jogador {self.skill_focus_player_id}')
        await match.sendToPlayer(
            data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Davi",
                    "message": "Você perdeu um ponto de fé",
                    'stillUntilDismiss': True
                }},
            player_id=self.skill_focus_player_id
        )
        skill_player_target = match._getPlayerById(self.skill_focus_player_id)
        if skill_player_target is not None:
            match.takeDamage(skill_player_target, 1)
            player = match._getPlayerById(self.in_game_id.split("_")[0])
            match.setDanoEmFe(player, skill_player_target, 1)


class C_Elias(C_Heros):
    slug = 'elias'

    def __init__(self, in_game_id: str):
        super().__init__(slug="elias", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                }
            },
            player_id=player.id
        )
        for _team in match.players_in_match:
            for _player in _team:
                if _player.id == match.move_now.player_move_id:
                    continue
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Elias",
                        "message": f"Elias está orando..."
                    }
                }, player_id=_player.id)

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                }
            },
            player_id=player.id
        )
        for _team in match.players_in_match:
            for _player in _team:
                if _player.id == match.move_now.player_move_id:
                    continue
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Elias",
                        "message": f"Elias está orando..."
                    }
                }, player_id=_player.id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        if not match.move_now.player_target_id:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Elias",
                    "message": f"Faltou sabedoria..."
                }
            }, player_id=match.move_now.player_move_id)
        else:
            player_target = match._getPlayerById(
                match.move_now.player_target_id)
            await match.moveCard(player_target, match.move_now.card_target_id, 'battle', 'forgotten')
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Elias",
                    "message": f"Sua carta foi destruída: {match.move_now.card_target_id.split('_')[1]}"
                }
            }, player_id=player_target.id)
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "2 Reis 1:12",
                    "message": f"Respondeu Elias: Se sou homem de Deus, que desça fogo do céu e consuma você e seus cinquenta soldados!... De novo fogo de Deus desceu e consumiu o oficial e seus soldados.",
                    "stillUntilDismiss": True
                }
            }, player_id=player_target.id)


class C_Ester(C_Heros):
    slug = 'ester'

    def __init__(self, in_game_id: str):
        super().__init__(slug="ester", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        __card_deck = []
        for __card in player.card_deck[:3]:
            __card_deck.append(__card.getStats())
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': __card_deck
                }
            },
            player_id=player.id
        )

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        __card_deck = []
        for __card in player.card_deck[:3]:
            __card_deck.append(__card.getStats())
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': __card_deck
                }
            },
            player_id=player.id
        )


class C_Eva(C_Heros):
    slug = 'eva'

    def __init__(self, in_game_id: str):
        super().__init__(slug="eva", in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        player = match._getPlayerById(match.move_now.player_move_id)
        card = match.giveCard(player, 1)
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Habilidade da Eva.",
                "message": f'Você comnprou a carta {card}.'
            }
        }, player_id=player.id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        await self.addSkill(match)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId('adao', player.card_prepare_camp)
        if card:
            await card.addSkill(match)
            Logger.info(msg="ADÃO está em jogo", tag='C_Card_Match')
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId('adao', player.card_battle_camp)
        if card:
            await card.addSkill(match)
            Logger.info(msg="ADÃO está em jogo", tag='C_Card_Match')

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        card = match.giveCard(player, 1)
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Habilidade da Eva.",
                "message": f'Você comnprou a carta {card}.'
            }
        }, player_id=player.id)
        # Procurar por Adão no campo de preparação
        card = getCardInListBySlugId('adao', player.card_prepare_camp)
        if card:
            await card.addSkill(match)
            Logger.info(msg="ADÃO está em jogo", tag='C_Card_Match')
        # Procurar por Adão no campo de batalha
        card = getCardInListBySlugId('adao', player.card_battle_camp)
        if card:
            await card.addSkill(match)
            Logger.info(msg="ADÃO está em jogo", tag='C_Card_Match')


class C_Jaco(C_Heros):
    slug = 'jaco'

    def __init__(self, in_game_id: str):
        super().__init__(slug="jaco", in_game_id=in_game_id)

    async def onAttack(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        player_target = match._getPlayerById(match.move_now.player_target_id)
        await super().onAttack(match)
        if len(player_target.card_hand) > 0:
            card_to_show = choice(player_target.card_hand)
            if card_to_show.card_type == 'miracle':
                match.giveCard(player, 1)
            await match.sendToPlayer(
                data={
                    'data_type': 'card_skill',
                    'card_data': {
                        'slug': self.slug,
                        'deck': [{'slug': card_to_show.slug, 'card_type': card_to_show.card_type}]
                    }
                },
                player_id=player.id
            )


class C_JoseDoEgito(C_Heros):
    slug = 'jose-do-egito'

    def __init__(self, in_game_id: str):
        super().__init__(slug="jose-do-egito", in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        player_target = match.fight_camp.player_defense
        await super().addSkill(match)
        if len(player_target.card_hand) < 1:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"O oponente não tem cartas para descartar."
                }
            }, player_id=match.fight_camp.player_attack.id)
        else:
            __card_to_discart = choice(player_target.card_hand)
            await match.moveCard(
                player=player_target,
                card_id=__card_to_discart.in_game_id,
                move_from='hand',
                move_to='forgotten'
            )
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"A carta {__card_to_discart.slug} foi descartada."
                }
            }, player_id=match.fight_camp.player_attack.id)
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"A carta {__card_to_discart.slug} foi descartada."
                }
            }, player_id=match.fight_camp.player_defense.id)

    async def rmvSkill(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().rmvSkill(match)
        gived_card: C_Card_Match = match.giveCard(player, 1)
        if gived_card:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f'Você comprou a carta {gived_card.slug}.'
                }
            }, player_id=match.fight_camp.player_attack.id)
        else:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de José do Egito",
                    "message": f"Não foi possível comprar uma carta."
                }
            }, player_id=match.fight_camp.player_attack.id)

    async def hasSuccessfullyAttacked(
            self,
            player: 'C_Player_Match',
            player_target: 'C_Player_Match',
            match: 'C_Match'):
        await super().hasSuccessfullyAttacked(player=player, player_target=player_target,  match=match)
        await self.addSkill(match=match)

    async def hasNotSuccessfullyAttacked(
            self,
            player: 'C_Player_Match',
            player_target: 'C_Player_Match',
            match: 'C_Match'):
        await super().hasNotSuccessfullyAttacked(player=player, player_target=player_target,  match=match)
        await self.rmvSkill(match=match)


class C_Josue(C_Heros):
    slug = 'josue'

    def __init__(self, in_game_id: str):
        super().__init__(slug="josue", in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        attack_cards = match.fight_camp.attack_cards
        await super().addSkill(match)
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Add 1/0 to {card.in_game_id}')
                card.attack_point += 1

    async def rmvSkill(self, match: 'C_Match'):
        attack_cards = match.fight_camp.attack_cards
        await super().rmvSkill(match)
        for card in attack_cards:
            if card.in_game_id != self.in_game_id:
                print(f'Remove 1/0 to {card.in_game_id}')
                card.attack_point -= 1

    async def onAttack(self, match: 'C_Match'):
        await super().onAttack(match)
        await self.addSkill(match)


class C_Maria(C_Heros):
    slug = 'maria'

    def __init__(self, in_game_id: str):
        super().__init__(slug="maria", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        __heros_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'hero':
                __heros_in_deck.append(__card.getStats())
        sorted_cards = sorted(__heros_in_deck, key=lambda card: card['slug'])
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_cards
                }
            },
            player_id=player.id
        )

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        __heros_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'hero':
                __heros_in_deck.append(__card.getStats())
        sorted_cards = sorted(__heros_in_deck, key=lambda card: card['slug'])
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_cards
                }
            },
            player_id=player.id
        )


class C_Moises(C_Heros):
    slug = 'moises'

    def __init__(self, in_game_id: str):
        super().__init__(slug="moises", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        __miracles_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'miracle':
                __miracles_in_deck.append(
                    {
                        'slug': __card.slug,
                        'in_game_id': __card.in_game_id
                    }
                )
        sorted_miracles_in_deck = sorted(
            __miracles_in_deck, key=lambda card: card['slug'])

        __miracles_in_forgoten_sea = []
        for __card_forgotten in player.card_in_forgotten_sea:
            if __card_forgotten.card_type == 'miracle':
                __miracles_in_forgoten_sea.append(
                    {
                        'slug': __card_forgotten.slug,
                        'in_game_id': __card_forgotten.in_game_id
                    }
                )
        sorted_miracles_in_forgoten_sea = sorted(
            __miracles_in_forgoten_sea, key=lambda card: card['slug'])
        if len(__miracles_in_forgoten_sea) == 0 and len(__miracles_in_deck) == 0:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de Moisés",
                    "message": f"Não há milagres."
                }
            }, player_id=player.id)
            return
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_miracles_in_deck,
                    'forgotten_sea': sorted_miracles_in_forgoten_sea,
                }
            },
            player_id=player.id
        )

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        __miracles_in_deck = []
        for __card in player.card_deck:
            if __card.card_type == 'miracle':
                __miracles_in_deck.append(
                    {
                        'slug': __card.slug,
                        'in_game_id': __card.in_game_id
                    }
                )
        sorted_miracles_in_deck = sorted(
            __miracles_in_deck, key=lambda card: card['slug'])

        __miracles_in_forgoten_sea = []
        for __card_forgotten in player.card_in_forgotten_sea:
            if __card_forgotten.card_type == 'miracle':
                __miracles_in_forgoten_sea.append(
                    {
                        'slug': __card_forgotten.slug,
                        'in_game_id': __card_forgotten.in_game_id
                    }
                )
        sorted_miracles_in_forgoten_sea = sorted(
            __miracles_in_forgoten_sea, key=lambda card: card['slug'])
        await match.sendToPlayer(
            data={
                'data_type': 'card_skill',
                'card_data': {
                    'slug': self.slug,
                    'deck': sorted_miracles_in_deck,
                    'forgotten_sea': sorted_miracles_in_forgoten_sea,
                }
            },
            player_id=player.id
        )

    async def addSkill(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().addSkill(match)
        card_id = match.move_now.card_list[0].get('in_game_id')
        if card_id is None:
            consolePrint.danger("Moisés: Não encontrou a carta")
        card_in_deck = getCardInListBySlugId(card_id, player.card_deck)
        card_in_sea = getCardInListBySlugId(
            card_id, player.card_in_forgotten_sea)
        print(card_in_deck, card_in_sea)
        if card_in_deck is not None:
            player.card_deck.remove(card_in_deck)
            player.card_hand.append(card_in_deck)
            card_in_deck.status = 'ready'
            for _team in match.players_in_match:
                for _player in _team:
                    if _player.id == player.id:
                        continue
                    await match.sendToPlayer(data={
                        'data_type': 'notification',
                        'notification': {
                            "title": "Habilidade de Moisés",
                            "message": f"Moisés antecipou a carta {card_in_deck.slug}."
                        }
                    }, player_id=_player.id)
        elif card_in_sea is not None:
            player.card_in_forgotten_sea.remove(card_in_sea)
            player.card_hand.append(card_in_sea)
            card_in_sea.status = 'ready'
            for _team in match.players_in_match:
                for _player in _team:
                    if _player.id == player.id:
                        continue
                    await match.sendToPlayer(data={
                        'data_type': 'notification',
                        'notification': {
                            "title": "Habilidade de Moisés",
                            "message": f"Moisés resgatou a carta {card_in_sea.slug}."
                        }
                    }, player_id=_player.id)


class C_Noe(C_Heros):
    slug = 'noe'

    def __init__(self, in_game_id: str):
        super().__init__(slug="noe", in_game_id=in_game_id)


class C_Salomao(C_Heros):
    slug = 'salomao'

    def __init__(self, in_game_id: str):
        super().__init__(slug="salomao", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        if player.wisdom_points < 10:
            player.wisdom_available += 1
            player.wisdom_points += 1
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de  Salomão",
                    "message": f"Você ganhou 1 ponto de sabedoria."
                }
            }, player_id=player.id)

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        if player.wisdom_points < 10:
            player.wisdom_available += 1
            player.wisdom_points += 1
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Habilidade de  Salomão",
                    "message": f"Você ganhou 1 ponto de sabedoria."
                }
            }, player_id=player.id)

    async def onAttack(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onAttack(match)
        if player.wisdom_available < player.wisdom_points:
            player.wisdom_available += 1


class C_Sansao(C_Heros):
    slug = 'sansao'

    def __init__(self, in_game_id: str):
        super().__init__(slug="sansao", in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        await super().onInvoke(match)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Habilidade de Sansão",
                "message": f"Sansão está pronto para atacar."
            }
        }, player_id=player.id)

    async def onResurrection(self, match: 'C_Match', player: 'C_Player_Match'):
        await super().onResurrection(match, player)
        await match.moveCard(player, self.in_game_id, 'prepare', 'battle')
        self.status = 'ready'
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Habilidade de Sansão",
                "message": f"Sansão está pronto para atacar."
            }
        }, player_id=player.id)
