from fastapi import WebSocket


class UserWSList:
    user_name: str = ''
    ws: list[int] = []


class WS_Manager:
    def __init__(self):
        self.conns: list[WebSocket] = []
        self.websocket_user_list: dict = {}

    async def connect(self, websocket: WebSocket, user: str = None):
        await websocket.accept()
        self.conns.append(websocket)
        if user:
            try:
                self.websocket_user_list[user].user_name = user
                self.websocket_user_list[user].ws = websocket
            except KeyError:
                self.websocket_user_list[user] = UserWSList()
                self.websocket_user_list[user].user_name = user
                self.websocket_user_list[user].ws = websocket
            finally:
                self.show_count(user)

    def disconnect(self, websocket: WebSocket, user: str = None):
        self.conns.remove(websocket)
        if user:
            self.websocket_user_list[user].ws = None

    async def broadcast(self, event, user: str = None):
        user = int(user)
        print(f"Broadcast para: {user}")
        print(f"Broadcasts disponíveis: {self.websocket_user_list}")
        try:
            if user:
                await self.websocket_user_list[user].ws.send_json(event)

            else:
                for ws in self.conns:
                    await ws.send_json(event)
        except KeyError as e:
            print("DEU ERRO NO WS", __file__)
            print("Chave não encontrada", e)
            print("Salvar a notificação no Banco de dados")
            # Salvar a notificação no Banco de dados
            return KeyError(e)
        except Exception as e:
            print("DEU ERRO NO WS", __file__, e)

    def show_count(self, user: str = None):
        print(f'{id(self.websocket_user_list[user].ws)} ws para {user}')
        return len(self.websocket_user_list[user].ws)
