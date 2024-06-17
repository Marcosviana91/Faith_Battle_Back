# Stage 2: The game is in curse
import asyncio

from models import Card
from models.schemas import GameData, GameRoomSchema, Players_in_Match


def moveToPrepare(player: Players_in_Match, card: Card, directlyToBattle: bool = False):
    if player.wisdom_points >= ( player.wisdom_used + card.card_wisdom_cost ):
        print(f'Move card {card} to prepare zone')
        if not directlyToBattle:
            player.card_hand.remove(card)
            player.card_prepare_camp.append(card)
        else:
            player.card_hand.remove(card)
            player.card_battle_camp.append(card)
        # SOMAR O CUSTO DA CARTA
        player.wisdom_used += card.card_wisdom_cost

    else:
        print('Sem sabedoria')


def moveToBattle(player: Players_in_Match, card: Card):
    player.card_prepare_camp.remove(card)
    player.card_battle_camp.append(card)


def dataHandle(self: GameRoomSchema, data: GameData):
    player = self.getPlayerByPlayerId(data.player_id)
    match data.data_type:
        case  "move":
            if (data.player_id == self.players_in_match[self.player_turn].id or (self.can_others_moves)):
                match data.move.move_type:
                    case 'move_to_prepare':
                        moveToPrepare(player, data.move.card_id)
                    case 'move_to_battle':
                        moveToBattle(player, data.move.card_id)

        case "ready":
            player.ready = True
            print(f"Player {data.player_id} has finished their turn.")
            self.player_turn += 1
            if self.player_turn < self.players_in_match.__len__():
                self.playerTurnHandle()
            else:
                self.newRoundHandle()
