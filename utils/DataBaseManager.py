import asyncio
import requests

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, Field

from settings import env_settings as env

# from utils.console import consolePrint

from schemas.users_schema import NewUserSchema
from schemas.API_schemas import APIResponseSchema
<<<<<<< HEAD
from schemas.players_schema import PlayersTinyDBSchema
from schemas.users_schema import NewUserSchema, UserPublic
from settings import env_settings
from utils import security

from utils.LoggerManager import Logger
from utils.console import consolePrint
=======

from utils.Cards.standard.raw_data import STANDARD_CARDS


class Deck(BaseModel):
    name: str = Field(alias='_id', default='standard')
    cards: list[str] = Field(default=STANDARD_CARDS)


STANDARD_DECK = Deck(**{
    '_id': 'standard',
    'cards': STANDARD_CARDS
})
UPPER_DECK = Deck(**{
    '_id': 'upper',
    'cards': STANDARD_CARDS[:12]
})
LOWER_DECK = Deck(**{
    '_id': 'lower',
    'cards': STANDARD_CARDS[12:]
})


class PlayerData(BaseModel):
    id: int = Field(alias="_id")
    avatar: int = Field(default=1)
    available_cards: list[str] = Field(default=STANDARD_CARDS)
    decks: list[Deck] | None = Field(
        default=[STANDARD_DECK, UPPER_DECK, LOWER_DECK])
    selected_deck: str | None = Field(default='standard')
    xp_points: int = Field(default=0)
    room_id: str | None = Field(default=None)
    match_id: str | None = Field(default=None)
>>>>>>> development


class DB_Manager:
    """
    Handle the data persistance
    """

    def __init__(self):
        client = AsyncIOMotorClient(
            host=env.DB_HOST,
            port=int(env.DB_PORT),
            username=env.DB_USER,
            password=env.DB_PASSWORD,
            server_api=ServerApi('1')
        )

        dbname = client[env.DB_NAME]
        self.all_players = dbname['players']

    async def getPlayerById(self, player_id: int):
        founded_player = await self.all_players.find_one({"_id": player_id})
        if founded_player is None:
            new_player = PlayerData(_id=player_id)
            user = requests.get(
                f'http://{env.DB_HOST}:3111/api/user/{player_id}')
            if user.status_code == 200:
                user = dict(user.json())
                new_player.avatar = int(user['last_name'])
            await self.all_players.insert_one(new_player.model_dump(by_alias=True))
            founded_player = await self.all_players.find_one({"_id": player_id})
        return founded_player

    async def getUserDataById(self, user_id: int):
        user = requests.get(f'http://{env.DB_HOST}:3111/api/user/{user_id}')
        if user.status_code == 200:
            player = await self.getPlayerById(user_id)
            user = dict(user.json())
            user.pop('last_name')
            user['avatar'] = player['avatar']
            user['xp_points'] = player['xp_points']
            user['available_cards'] = player['available_cards']
            user['decks'] = player['decks']
            user['selected_deck'] = player['selected_deck']
            if player['room_id']:
                user['room_id'] = player['room_id']
            if player['match_id']:
                user['match_id'] = player['match_id']

        return user

    # UPDATE DB DATA
    async def setPlayerRoomOrMatch(self, player_id: int, room_id: str = None, match_id: str = None, clear:bool = False):
        founded_player = await self.getPlayerById(player_id)
        if room_id:
            founded_player['room_id'] = room_id
        if match_id:
            founded_player['match_id'] = match_id
        if clear:
            founded_player['room_id'] = None
            founded_player['match_id'] = None
        self.all_players.update_one(
            {"_id": player_id},
            {"$set": founded_player}
        )

    def createNewUser(self, data: NewUserSchema) -> APIResponseSchema:
<<<<<<< HEAD
        response = APIResponseSchema(message="User not created")
        newUser = models.UserModel(**(data.model_dump()))
        newUser.username = newUser.username.lower()
        with Session(self.engine) as session:
            query_username = select(models.UserModel).where(
                models.UserModel.username == newUser.username
            )
            check_username = session.exec(query_username)
            # query_email = select(models.UserModel).where(
            #     models.UserModel.email == newUser.email
            # )
            # check_email = session.exec(query_email)

            if len(check_username.all()) > 0:
                # print("username already exists")
                response.data_type = "error"
                response.message = "username already exists"

            # if len(check_email.all()) > 0:
            #     # print("email already in use")
            #     response.data_type = "error"
            #     if response.message == "username already exists":
            #         response.message = (
            #             "username already exists\nemail already in use"
            #         )
            #     else:
            #         response.message = "email already in use"

            else:
                # print("user successful created")
                newUser.password = security.encrypt(data.password)
                session.add(newUser)
                session.commit()
                session.refresh(newUser)

                self.createDefaultPlayerStats(player_id=newUser.id)
                response.data_type = "user_created"
                response.message = "user successful created"
                response.user_data = UserPublic(**newUser.model_dump())
                Logger.info(f'New user created {newUser.id}: {newUser.username}.', 'DB')

=======
        response = APIResponseSchema()
        newUser = requests.post(f'http://{env.DB_HOST}:3111/api/user',
                                json={'username': data.username.lower(), 'password': data.password, 'first_name': data.first_name, 'avatar': data.avatar})
        if newUser.status_code == 200:
            response.data_type = 'user_data'
            response.user_data = newUser.json()
>>>>>>> development
        return response

    # def updateUser(
    #     self, user_id: int, user_new_data: NewUserSchema
    # ) -> APIResponseSchema:
    #     response = APIResponseSchema(message="user not updated")
    #         player_data = PlayerData(**founded_player)
    #         print(player_data)
    #     return response


DB = DB_Manager()
