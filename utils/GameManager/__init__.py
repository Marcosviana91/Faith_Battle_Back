from random import shuffle
from datetime import datetime

from schemas import GameSchema, GameRoomSchema, CardSchema
from .stages import stage0, stage1, stage2


MAXIMUM_FAITH_POINTS = 15


def printCard(list_name: str, card_list: list[CardSchema]):
    _list = []
    for card in card_list:
        _list.append(card.card_slug)
    print(f'{list_name}: {_list}')


class GameRoom(GameRoomSchema):

    def gameHandle(self, data: GameSchema):
        # print(__file__,"\n", data)
        match self.game_stage:
            case 0:
                return stage0.dataHandle(self, data)
            case 1:
                return stage1.dataHandle(self, data)
            case 2:
                return stage2.dataHandle(self, data)
        return {
            "type": 'error',
            "message": f'Something has going wrong in {__file__} GameRoom.gameHandle'
        }

    def gameStart(self):
        print('Starting game...')
        self.start_match = datetime.now().timestamp()
        for player in self.players_in_match:
            # shuffle(player.card_deck)
            player.faith_points = MAXIMUM_FAITH_POINTS
        # shuffle(self.players_in_match)
        self.newRoundHandle()

    def newRoundHandle(self):
        self.round += 1
        print(f"\n\nROUND {self.round}. . . . . \n")
        # Mais 1 de sabedoria para cada jogador
        for player in self.players_in_match:
            player.wisdom_points += 1
            print(f'Player {player.id}')
            # printCard('Deck', player.card_deck)
            # printCard('Mão', player.card_hand)
            # printCard('Preparação', player.card_prepare_camp)
            # printCard('Batalha', player.card_battle_camp)
            # printCard('Esquecimento', player.card_in_forgotten_sea)
        self.player_turn = 0
        self.playerTurnHandle()

    def playerTurnHandle(self):
        print(f'Player {self.players_in_match[self.player_turn].id} turn:')
        player = self.players_in_match[self.player_turn]
        player.wisdom_used = 0
        self.giveCard(player, 1)
        
