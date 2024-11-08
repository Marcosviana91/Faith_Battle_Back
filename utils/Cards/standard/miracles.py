import asyncio  # Usado por Diluvio
from typing import TYPE_CHECKING, List

from .base_cards import C_Card_Match, getCardInListBySlugId

from utils.console import consolePrint

if TYPE_CHECKING:
    from utils.MATCHES.MatchClass import C_Match


class C_Miracles(C_Card_Match):

    def __init__(self, slug: str, in_game_id: str):
        super().__init__(slug, in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        player = match._getPlayerById(match.move_now.player_move_id)
        player.usou_milagres.append(self.slug)
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
        player = match._getPlayerById(self.card_move.player_target_id)
        await super().addSkill(match)
        player.card_prepare_camp.remove(self)
        player.card_in_forgotten_sea.append(self)
        self.reset()


class C_CordeiroDeDeus(C_Miracles):
    slug = 'cordeiro-de-deus'

    def __init__(self, in_game_id: str):
        super().__init__(slug='cordeiro-de-deus', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Até seu próximo turno, o jogador alvo não perde pontos de fé, pecados não o afetam e suas cartas são indestrutívies
        player_target = match._getPlayerById(self.card_move.player_target_id)
        player_target.fe_inabalavel = True
        player_target.incorruptivel = True
        for _card in player_target.card_battle_camp:
            _card.indestrutivel = True
        player_target.attached_effects.append(self)
        
    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        player_target = match._getPlayerById(self.card_move.player_target_id)
        player_target.fe_inabalavel = False
        player_target.incorruptivel = False
        for _card in player_target.card_battle_camp:
            _card.indestrutivel = False
        player_target.attached_effects.remove(self)


class C_Diluvio(C_Miracles):
    slug = 'diluvio'

    def __init__(self, in_game_id: str):
        super().__init__(slug='diluvio', in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        for _team in match.players_in_match:
            for _player in _team:
                # if _player.id == match.move_now.player_move: continue
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Dilúvio",
                        "message": f"Parece que vai chover..."
                    }
                }, player_id=_player.id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # player_target = match._getPlayerById(match.move_now.player_target_id)
        # Destrói todos os heróis e artefatos da zona de batalha. Noé e a Arca sobrevivem
        # Verificar Arca de Noé dentre as cartas acopladas aos heróis - FALTA
        all_tasks = []
        for _team in match.players_in_match:
            for player_target in _team:
                _card_list_whitout_noe = list(
                    filter(lambda _card: _card.slug != 'noe', player_target.card_battle_camp))
                _card_list_whitout_arca_de_noe: List[C_Card_Match] = []
                for __card in _card_list_whitout_noe:
                    if getCardInListBySlugId('arca-de-noe', __card.attached_cards):
                        continue
                    _card_list_whitout_arca_de_noe.append(__card)
                player_tasks = [await match.moveCard(player=player_target, card_id=_card.in_game_id,
                                                     move_from='battle', move_to='forgotten') for _card in _card_list_whitout_arca_de_noe]
                all_tasks = [*all_tasks, *player_tasks]
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Gênesis: 7:23",
                        "message": f"O dilúvio destruiu todo ser vivo da face da Terra, homens e animais foram exterminados. Só restaram Noé e aqueles que com ele estavam na Arca.",
                        "stillUntilDismiss": True
                    }
                }, player_id=player_target.id)
        try:
            await asyncio.wait(all_tasks)
        except AttributeError as e:
            consolePrint.danger(f'MIRACLE: AttributeError {e}')


class C_FogoDoCeu(C_Miracles):
    slug = 'fogo-do-ceu'

    def __init__(self, in_game_id: str):
        super().__init__(slug='fogo-do-ceu', in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        for _team in match.players_in_match:
            for _player in _team:
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Fogo do Céu",
                        "message": f"O que é aquilo brilhando no céu?"
                    }
                }, player_id=_player.id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        player_target_id = self.card_move.player_target_id
        if not player_target_id:
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Fogo no Céu",
                    "message": f"Faltou sabedoria..."
                }
            }, player_id=match.move_now.player_move_id)
        else:
            player_target = match._getPlayerById(player_target_id)
            # Destrói uma carta da zona de batalha
            # Mesma habilidade de Elias
            card_target_id: str = self.card_move.card_target_id
            await match.moveCard(player_target, card_target_id, 'battle', 'forgotten')
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Fogo do Céu",
                    "message": f"A carta {card_target_id.split('_')[1]} foi destruída"
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
            consolePrint.status(
                f'A carta {card_target_id} foi destruída')
            # Verificar heróis em batalha
            if match.fight_camp:
                match.fight_camp.destroyHeroBeforeFight(card_target_id)


class C_ForcaDeSansao(C_Miracles):
    slug = 'forca-de-sansao'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def onInvoke(self, match: 'C_Match'):
        await super().onInvoke(match)
        for _team in match.players_in_match:
            for _player in _team:
                await match.sendToPlayer(data={
                    'data_type': 'notification',
                    'notification': {
                        "title": "Força de Sansão",
                        "message": f"O monstro vai sair da jaula..."
                    }
                }, player_id=_player.id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # O herói alvo ganha 3/3 até o final do turno. Se o alvo é Sansão, ele se torna indestrutível até o final do turno.
        player_target_id = self.card_move.player_target_id
        card_target_id: str = self.card_move.get('card_target_id')
        player_target = match._getPlayerById(player_target_id)
        card_hero = getCardInListBySlugId(
            card_target_id, player_target.card_battle_camp)
        card_hero.attached_effects.append(self)
        card_hero.attack_point += 3
        card_hero.defense_point += 3
        if card_hero.slug == 'sansao':
            card_hero.indestrutivel = True

    async def rmvSkill(self, match: 'C_Match'):
        await super().rmvSkill(match)
        # O herói alvo ganha 3/3 até o final do turno. Se o alvo é Sansão, ele se torna indestrutível até o final do turno.
        player_target_id = self.card_move.player_target_id
        card_target_id: str = self.card_move.card_target_id
        player_target = match._getPlayerById(player_target_id)
        card_hero = getCardInListBySlugId(
            card_target_id, player_target.card_battle_camp)
        card_hero.attached_effects.remove(self)
        card_hero.attack_point -= 3
        card_hero.defense_point -= 3
        if card_hero.slug == 'sansao':
            card_hero.indestrutivel = False


class C_LiberacaoCelestial(C_Miracles):
    slug = 'liberacao-celestial'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Anula qualquer efeito de milagre ou pecado nesse instante.


class C_NoCeuTemPao(C_Miracles):
    slug = 'no-ceu-tem-pao'

    def __init__(self, in_game_id: str):
        super().__init__(slug='no-ceu-tem-pao', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        player_target = match._getPlayerById(
            self.card_move.player_target_id)
        # O jogador alvo compra 3 cartas, se voce tem moisés em sua zona de batalha, compre 5.
        match.giveCard(player_target, 3)
        card = getCardInListBySlugId('moises', player_target.card_battle_camp)
        if card:
            match.giveCard(player_target, 2)


class C_PassagemSegura(C_Miracles):
    slug = 'passagem-segura'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Os heróis do jogador alvo são imbloqueáveis neste turno


class C_ProtecaoDivina(C_Miracles):
    slug = 'protecao-divina'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # O jogador alvo não sofre dano de efeitos ou ataque de Heróis neste turno


class C_Ressurreicao(C_Miracles):
    slug = 'ressurreicao'

    def __init__(self, in_game_id: str):
        super().__init__(slug=self.slug, in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        await super().addSkill(match)
        # Retorna um herói de qualquer mar do esquecimento ao jogo sob seu controle. Voce escolhe em qual zona ele voltará.
        player_target = match._getPlayerById(self.card_move.            player_target_id)  # Jogador que vai receber a carta
        player_target2 = match._getPlayerById(self.card_move.player_target2_id)  # Jogador que vai ceder a carta
        card_target_id: str = self.card_move.get('card_target_id')
        card_hero = getCardInListBySlugId(
            card_target_id, player_target2.card_in_forgotten_sea) # Herói que vai ressucitar
        player_target2.card_in_forgotten_sea.remove(card_hero)
        player_target.card_prepare_camp.append(card_hero)
        old_card_id = card_hero.in_game_id.split("_")
        card_hero.in_game_id = f'{player_target.id}_{old_card_id[1]}_{old_card_id[2]}'
        await card_hero.onResurrection(player=player_target, match=match)


class C_RestauracaoDeFe(C_Miracles):
    slug = 'restauracao-de-fe'

    def __init__(self, in_game_id: str):
        super().__init__(slug='restauracao-de-fe', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        player_target = match._getPlayerById(
            self.card_move.get('player_target_id'))
        await super().addSkill(match)
        # O jogador alvo ganha um ponto de fé por cada herói no campo de batlaha dele.
        faith_count = 0
        for _card in player_target.card_battle_camp:
            if _card.card_type == 'hero':
                faith_count += 1
        player_target.faith_points += faith_count
        player_target.fe_recebida += faith_count
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Restauração de Fé.",
                "message": f'Você ganhou {faith_count} pontos de fé.'
            }
        }, player_id=player_target.id)
        consolePrint.info(f'O jogador {player_target.id} ganhou {
                          faith_count} pontos de fé.')


class C_SabedoriaDeSalomao(C_Miracles):
    slug = 'sabedoria-de-salomao'

    def __init__(self, in_game_id: str):
        super().__init__(slug='sabedoria-de-salomao', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        player_target = match._getPlayerById(
            self.card_move.player_target_id)
        await super().addSkill(match)
        # O jogador alvo reativa 3 cartas de sabedoria.
        player_target.wisdom_available += 3
        if player_target.wisdom_available > player_target.wisdom_points:
            player_target.wisdom_available = player_target.wisdom_points
        # Se Salomão está em jogo, compre uma carta.
        salomao_in_prepare = getCardInListBySlugId(
            'salomao', player_target.card_prepare_camp)
        salomao_in_battle = getCardInListBySlugId(
            'salomao', player_target.card_battle_camp)
        if salomao_in_battle or salomao_in_prepare:
            consolePrint.info('MIRACLE: Compra 1 carta')
            gived_card: C_Card_Match = match.giveCard(player=player_target)
            await match.sendToPlayer(data={
                'data_type': 'notification',
                'notification': {
                    "title": "Sabedoria de Salomão",
                    "message": f'Você comprou a carta {gived_card.slug}.'
                }
            }, player_id=player_target.id)


class C_SarcaArdente(C_Miracles):
    slug = 'sarca-ardente'

    def __init__(self, in_game_id: str):
        super().__init__(slug='sarca-ardente', in_game_id=in_game_id)

    async def addSkill(self, match: 'C_Match'):
        player_target = match._getPlayerById(
            self.card_move.player_target_id)
        player_target2 = match._getPlayerById(
            self.card_move.player_target2_id)
        await super().addSkill(match)
        # O jogador alva ganha 2 pontos de fé e o oponente alvo perde 2 pontos de fé
        player_target.faith_points += 2
        player_target.fe_recebida += 2
        match.takeDamage(player_target2, 2)
        match.setDanoEmFe(player_target, player_target2, 2)
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Sarça Ardente",
                "message": f'Você ganhou 2 pontos de Fé.'
            }
        }, player_id=player_target.id)
        await match.sendToPlayer(data={
            'data_type': 'notification',
            'notification': {
                "title": "Sarça Ardente",
                "message": f'Você perdeu 2 pontos de Fé.'
            }
        }, player_id=player_target2.id)
