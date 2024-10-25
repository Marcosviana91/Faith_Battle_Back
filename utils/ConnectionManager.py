from fastapi import WebSocket
from pprint import pprint
from schemas.users_schema import UserWs
from utils.LoggerManager import Logger
from utils.security import getCurrentUserAuthenticated

from utils.Cards.standard.raw_data import STANDARD_CARDS_RAW_DATA

from random import shuffle

CARDS_DATA = {
    'cards': [
    ]
}


for key in STANDARD_CARDS_RAW_DATA:
    # print(
    #     {
    #         'slug': key,
    #         'in_game_id': "",
    #         'where_i_am': 'deck',
    #         'attack_point': STANDARD_CARDS_RAW_DATA[key][2],
    #         'defense_point': STANDARD_CARDS_RAW_DATA[key][3],
    #         'wisdom_cost': STANDARD_CARDS_RAW_DATA[key][1],
    #     }
    # )
    CARDS_DATA['cards'].append(
        {
            'slug': key,
            'in_game_id': "",
            'where_i_am': 'deck',
            'attack_point': STANDARD_CARDS_RAW_DATA[key][2],
            'defense_point': STANDARD_CARDS_RAW_DATA[key][3],
            'wisdom_cost': STANDARD_CARDS_RAW_DATA[key][1],
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
        elif self.all_room.get(room):
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
            await self.send2Room(room=room, data={
                'data_type': 'start',
                'cards': self.generateCards(room=room)
            })
        # print('\nStats')
        # pprint(self.all_room)

    def disconnect(self, name: str, room: str):
        print(f'disconect player {name} from room {room}')
        # jogador_1 = self.all_room['room']['jogador_1']
        # jogador_2 = self.all_room['room']['jogador_2']

    async def send2Room(self, room: str, data: dict):
        print('SEND >>>: ', data)
        _room = self.all_room.get(room)
        try:
            await _room['jogador_1']['ws'].send_json(data)
            await _room['jogador_2']['ws'].send_json(data)
        except Exception as e:
            print("ERROR - send2Room:", e)


WS = WS_Manager()

WSFlat = WS_Flat_Manager()
