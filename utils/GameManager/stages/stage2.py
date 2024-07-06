# Stage 2: The game is in curse
import asyncio

from schemas import GameSchema, GameRoomSchema, PlayersInMatchSchema, CardSchema


def moveToPrepare(player: PlayersInMatchSchema, card: CardSchema, directlyToBattle: bool = False):
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


def moveToBattle(player: PlayersInMatchSchema, card: CardSchema):
    player.card_prepare_camp.remove(card)
    player.card_battle_camp.append(card)


def dataHandle(self: GameRoomSchema, data: GameSchema):
    player = self.getPlayerByPlayerId(data.player_id)
    match data.data_type:
        case  "move":
            if (data.player_id == self.PlayersInMatchSchema[self.player_turn].id or (self.can_others_moves)):
                match data.move.move_type:
                    case 'move_to_prepare':
                        moveToPrepare(player, data.move.card_id)
                    case 'move_to_battle':
                        moveToBattle(player, data.move.card_id)

        case "ready":
            player.ready = True
            print(f"Player {data.player_id} has finished their turn.")
            self.player_turn += 1
            if self.player_turn < self.PlayersInMatchSchema.__len__():
                self.playerTurnHandle()
            else:
                self.newRoundHandle()
