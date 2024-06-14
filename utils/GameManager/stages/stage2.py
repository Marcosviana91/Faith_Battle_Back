# Stage 2: The game is in curse
import asyncio

from models.schemas import GameData, GameRoomSchema, Players_in_Match


def moveToPrepare(player: Players_in_Match, card_id: int, directlyToBattle: bool = False):
    if not directlyToBattle:
        player.card_hand.remove(card_id)
        player.card_prepare_camp.append(card_id)
    else:
        player.card_hand.remove(card_id)
        player.card_battle_camp.append(card_id)
        
    print(f'Mão: {player.card_hand}')
    print(f'Pre: {player.card_prepare_camp}')
    print(f'Bat: {player.card_battle_camp}')

def moveToBattle(player: Players_in_Match, card_id: int):
    player.card_prepare_camp.remove(card_id)
    player.card_battle_camp.append(card_id)
    print(player.card_prepare_camp)
    print(player.card_battle_camp)

def dataHandle(self: GameRoomSchema, data: GameData):
    player = self.getPlayerByPlayerId(data.player_id)
    match data.data_type:
        case  "move":
            if (data.player_id == self.players_in_match[self.player_turn].id or (self.can_others_moves)):
                match data.move.move_type:
                    case 'move_to_prepare':
                        print(f'Move card {data.move.card_id} to prepare zone')
                        moveToPrepare(player, data.move.card_id)

        case "ready":
            player.ready = True
            print(f"Player {data.player_id} has finished their turn.")
            self.player_turn += 1
            if self.player_turn < self.players_in_match.__len__():
                self.playerTurnHandle()
            else:
                self.newRoundHandle()
