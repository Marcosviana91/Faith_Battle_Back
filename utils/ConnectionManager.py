from schemas.users_schema import UserWs
from utils.console import consolePrint


class WS_Manager:
    def __init__(self):
        self.all_users: list[UserWs] = []

    def __getUserWsById(self, user_id: int) -> UserWs:
        for user in self.all_users:
            if user.id == user_id:
                return user
        consolePrint.danger(msg=f'WS: User {user_id} not connected in WS')
        return None

    # Sem WS
    def login(self, user_ws: UserWs):
        user = self.__getUserWsById(user_ws.id)
        if user:
            self.all_users.remove(user)
        self.all_users.append(user_ws)
        consolePrint.info(msg=f"WS: User {user_ws.id} has logged in.")

    # Com WS
    def connect(self, user_ws: UserWs):
        # print(user_ws)
        user = self.__getUserWsById(user_ws.id)
        if user:
            if user.token == user_ws.token:
                user.websocket = user_ws.websocket
                consolePrint.info(
                    msg=f"WS: User {user_ws.id} has connected.")
                consolePrint.info(
                    msg=f"WS: Users connected in game: {
                        self.all_users.__len__()}."
                )
            else:
                user_ws.websocket.close()
                consolePrint.danger("token not match")
        # self.login(user_ws)

    def disconnect(self, user_id: int = None):
        user = self.__getUserWsById(user_id)
        if user:
            user.websocket = None
            self.all_users.remove(user)
            consolePrint.status(msg=f"WS: User {user_id} has disconnected.")
        consolePrint.info(msg=f"WS: Users connected in game: {
            self.all_users.__len__()}.")

    async def sendToPlayer(self, data: dict, user_id: int):
        user = self.__getUserWsById(user_id)
        if user:
            # consolePrint.info(f"WS: Send to player {user_id} {data.get('data_type')}")
            await user.websocket.send_json(data)

    # async def sendToAll(self, message):
    #     for user in self.all_users:
    #         await user.websocket.send_json(message)


WS = WS_Manager()
