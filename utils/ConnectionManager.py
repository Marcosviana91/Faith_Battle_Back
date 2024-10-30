from fastapi import WebSocket
from pprint import pprint
from schemas.users_schema import UserWs
from utils.LoggerManager import Logger
from utils.security import getCurrentUserAuthenticated

# Pegar esses dados da API do Django
from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

from random import shuffle

CARDS_DATA = {
    'cards': [
    ]
}


for key in STANDARD_CARDS_RAW_DATA:
    CARDS_DATA['cards'].append(
        {
            'slug': key,
            'in_game_id': "",
            'where_i_am': 'deck',
            # TODO: pegar start position da API do Django
            'position': {'left': 437, 'bottom': 188},
            'bottom_left_value': STANDARD_CARDS_RAW_DATA[key][2],
            'bottom_right_value': STANDARD_CARDS_RAW_DATA[key][3],
            'top_left_value': STANDARD_CARDS_RAW_DATA[key][1],
        }
    )


class WS_Manager:
    def __init__(self):
        self.all_users: list[UserWs] = []

    def __getUserWsById(self, user_id: int) -> UserWs:
        for user in self.all_users:
            if user.id == user_id:
                return user
        return None

    def getStats(self):
        data = []
        for user in self.all_users:
            data.append(user.id)
        return data

    async def connect(self, user_ws: UserWs):
        authenticated_user_id = getCurrentUserAuthenticated(
            user_ws.access_token)
        if authenticated_user_id is None:
            await user_ws.websocket.send_json({"data_type": "token_expired"})
            user_ws.websocket.close()
            return
        if authenticated_user_id != user_ws.id:
            Logger.danger(msg=f'Token não combina com o usuário {
                          user_ws.id}', tag='WS')
            user_ws.websocket.close()
            return
        user = self.__getUserWsById(user_ws.id)
        if user:
            user.websocket = user_ws.websocket
        else:
            self.all_users.append(user_ws)
        Logger.info(msg=f"Usuário {
                    user_ws.id} conectou usando um token", tag="AUTH")
        Logger.info(msg=f"Usuários conectados ao jogo: {
                    self.all_users.__len__()}", tag="WS")

    def disconnect(self, user_id: int = None):
        user = self.__getUserWsById(user_id)
        if user:
            user.websocket = None
            self.all_users.remove(user)
            Logger.info(msg=f"Usuário {
                        user_id} se desconectou do jogo.", tag="WS")
        Logger.info(msg=f"Usuários conectados ao jogo: {
                    self.all_users.__len__()}", tag="WS")

    async def sendToPlayer(self, data: dict, user_id: int):
        user = self.__getUserWsById(user_id)
        if user:
            # consolePrint.info(f"WS: Send to player {user_id} {data.get('data_type')}")
            await user.websocket.send_json(data)


class WS_Flat_Manager:
    def __init__(self):
        self.all_room = {}

    def generateCards(self, room):
        cards = {
        }
        # print(self.all_room[room])
        for jogador in self.all_room[room]:
            nome = self.all_room[room][jogador]['nome']
            cards[nome] = []
            # print(jogador, nome)
            for index, card in enumerate(CARDS_DATA['cards']):
                _card = dict(**card)
                _card['in_game_id'] = f'{nome}_{card['slug']}_{index}'
                cards[nome].append(_card)
            shuffle(cards[nome])
            # for _card_mao in cards[nome][:5]:
            #     _card_mao['where_i_am'] = 'mao'
            #     print(_card_mao)

        # print(cards)
        return cards

    async def connect(self, name: str, room: str, websocket: WebSocket):
        # print(f"Connecting player {name} in room {room}")
        if name == 'clear' and room == 'all':
            self.all_room = {}
            print('All rooms cleared...')
            return
        if self.all_room.get(room):
            # print(f"Ja tem a sala {room}")
            _room = dict(self.all_room.get(room))
            # pprint(_room)
            jogador_1 = _room.get('jogador_1')
            # pprint(jogador_1)
            jogador_2 = _room.get('jogador_2')
            # pprint(jogador_2)
            if jogador_1['nome'] == "" or jogador_1['nome'] == name:
                # print(f'jogador_1 {name} já conectado...')
                self.all_room.update({room: {
                    'jogador_1': {
                        'nome': name,
                        'ws': websocket,
                    },
                    'jogador_2': jogador_2,
                }})
            elif jogador_2['nome'] == "" or jogador_2['nome'] == name:
                # print(f'jogador_2 {name} já conectado...')
                self.all_room.update({room: {
                    'jogador_1': jogador_1,
                    'jogador_2': {
                        'nome': name,
                        'ws': websocket,
                    },
                }})
            else:
                print('SALA CHEIA')
        else:
            print(f'Criando a sala {room}')
            self.all_room.update({room: {
                'jogador_1': {
                    'nome': name,
                    'ws': websocket,
                },
                'jogador_2': {
                    'nome': '',
                    'ws': '',
                },
            }})
        jogador_1_ws = self.all_room[room]['jogador_1']['ws']
        jogador_2_ws = self.all_room[room]['jogador_2']['ws']
        if jogador_1_ws and jogador_2_ws:
            # print(jogador_1_ws, jogador_2_ws)
            print('iniciar partida')
            self.all_room.update({room: {
                'jogador_1': self.all_room[room]['jogador_1'],
                'jogador_2': self.all_room[room]['jogador_2'],
                'cards': self.generateCards(room=room)
            }})
            data_to_send = {
                'data_type': 'start',
                'cards': self.all_room.get(room)['cards']
            }
            # print(data_to_send)
            await self.send2Room(room=room, data=data_to_send)
        # print('\nStats')
        # pprint(self.all_room)

    def disconnect(self, name: str, room: str):
        print(f'disconect player {name} from room {room}')
        # jogador_1 = self.all_room['room']['jogador_1']
        # jogador_2 = self.all_room['room']['jogador_2']

    async def giveCards(self, sala: str, name: str):
        _sala = dict(self.all_room.get(sala))
        # print(_sala['cards'][name])
        card_to_give = None
        for card in _sala['cards'][name]:
            if card['where_i_am'] == 'deck':
                card.update({
                    'where_i_am': 'hand',
                    # 'position': {'left': 0, 'bottom': 0}
                })
                card_to_give = card
                break
        print(card_to_give)
        if card_to_give:
            data_to_send = {
                'data_type': 'give_card',
                'player': name,
                'card': card
            }
            await self.send2Room(room=sala, data=data_to_send)
        # TODO: resposta de sem cartas no deck

    async def send2Room(self, room: str, data: dict):
        import pprint
        print('SEND >>>: ')
        pprint.pprint(data['data_type'])
        _room = self.all_room.get(room)
        try:
            # if (data['data_type'] =='card_move'):
            #     print('Enviar DATA individualmente: ')
            #     print(data['player'])
            #     for jogador in _room:
            #         if (data['player']) != _room[jogador]['nome']:
            #             print(f'Enviar para {jogador}: ')
            #             await _room[jogador]['ws'].send_json(data)
            # else:
            #     print('Enviar DATA para TODOS')
            for jogador in _room:
                if jogador == 'cards':
                    continue
                await _room[jogador]['ws'].send_json(data)
        except Exception as e:
            print("ERROR - send2Room:", e)


WS = WS_Manager()

WSFlat = WS_Flat_Manager()
