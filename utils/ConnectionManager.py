from schemas.users_schema import UserWs


class WS_Manager:
    def __init__(self):
        self.all_users: list[UserWs] = []

    def __getUserWsById(self, user_id: int) -> UserWs:
        for user in self.all_users:
            if user.id == user_id:
                return user
        raise IndexError("user id not found")

    def login(self, user_ws: UserWs):
        try:
            user = self.__getUserWsById(user_ws.id)
            self.all_users.remove(user)
        except Exception:
            ...
        finally:
            self.all_users.append(user_ws)
            print(f"WS: User {user_ws.id} has logged in.")

    def connect(self, user_ws: UserWs):
        # print(user_ws)
        try:
            user = self.__getUserWsById(user_ws.id)
            if user.token == user_ws.token:
                user.websocket = user_ws.websocket
            else:
                user_ws.websocket.close()
                raise AssertionError("token not match")
        except Exception as e:
            print(f'{e}')
        print(f"WS: User {user_ws.id} has connected.")
        print(f"WS: Users connected in game: {
              self.all_users.__len__()}.")

    def disconnect(self, user_id: int = None):
        user = self.__getUserWsById(user_id)
        user.websocket = None
        self.all_users.remove(user)
        print(f"WS: User {user_id} has disconnected.")
        print(f"WS: Users connected in game: {
              self.all_users.__len__()}.")

    async def sendToPlayer(self, data: dict, user_id: int):
        try:
            user = self.__getUserWsById(user_id)
            # print(f"WS: Send to player {user_id}")
            await user.websocket.send_json(data)
        except IndexError as e:
            print(f"{e}: Player {user_id} not conected.")

    # async def sendToAll(self, message):
    #     for user in self.all_users:
    #         await user.websocket.send_json(message)


WS = WS_Manager()
