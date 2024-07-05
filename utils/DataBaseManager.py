from sqlmodel import Session, SQLModel, create_engine, select
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

# from settings import Settings
import models
from schemas import (
    APIResponseProps,
    APIResponseSchema,
    Player,
    UserPublic,
    UserSchema,
)
from settings import env_settings
from utils import security


class DB_Manager:
    """
    Handle the data persistance
    """

    def __init__(self):
        self.tiny_engine = TinyDB(
            "./database/database.json",
            sort_keys=True,
        )
        self.sqlite_url = "sqlite:///database/database.db"
        if env_settings.ENVIROMENT_TYPE == "DEV":
            self.tiny_engine = TinyDB(storage=MemoryStorage)
            # self.sqlite_url = "sqlite:///:memory:"

        self.engine = create_engine(self.sqlite_url)
        SQLModel.metadata.create_all(self.engine)
        if env_settings.ENVIROMENT_TYPE == "DEV":
            self.cleanUser()

    def cleanUser(self):
        with Session(self.engine) as session:
            query = select(models.UserModel)
            users = session.exec(query).all()
            for user in users:
                print(user)
                session.delete(user)
                session.commit()

    def createNewUser(self, data: UserSchema) -> APIResponseSchema:
        response = APIResponseSchema(message="User not created")
        newUser = models.UserModel(**(data.model_dump()))
        newUser.username = newUser.username.lower()
        with Session(self.engine) as session:
            query_username = select(models.UserModel).where(
                models.UserModel.username == newUser.username
            )
            check_username = session.exec(query_username)
            query_email = select(models.UserModel).where(
                models.UserModel.email == newUser.email
            )
            check_email = session.exec(query_email)

            if len(check_username.all()) > 0:
                # print("username already exists")
                response.data_type = "error"
                response.message = "username already exists"

            if len(check_email.all()) > 0:
                # print("email already in use")
                response.data_type = "error"
                if response.message == "username already exists":
                    response.message = (
                        "username already exists\nemail already in use"
                    )
                else:
                    response.message = "email already in use"

            else:
                # print("user successful created")
                newUser.password = security.encrypt(data.password)
                session.add(newUser)
                session.commit()

                self.createDefaultPlayerStats(player_id=newUser.id)
                response.data_type = "user_created"
                response.message = "user successful created"
                response.user_data = UserPublic(**newUser.model_dump())

        return response

    def updateUser(
        self, user_id: int, user_new_data: UserSchema
    ) -> APIResponseSchema:
        response = APIResponseSchema(message="user not updated")
        with Session(self.engine) as session:
            query_user_data = select(models.UserModel).where(
                models.UserModel.id == user_id
            )
            try:
                user = session.exec(
                    query_user_data
                ).one()  # Possível erro de usuário não encontrado

                user.email = user_new_data.email
                user.real_name = user_new_data.real_name
                user.username = user_new_data.username
                if user_new_data.password != "__not-change__":
                    user.password = security.encrypt(user_new_data.password)

                session.add(user)
                session.commit()
                response.data_type = "user_updated"
                response.message = "User data has been updated. Need logout."
            except Exception as e:
                response.message = e
                print(e)
        return response

    # Não acessado pela API
    # será criado outro script para verificar um usuário
    # que não loga há mais de X dias e o exclui do DB
    def deleteUser(self, user_id: int) -> APIResponseProps:
        response = APIResponseProps(message="username not found")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.id == user_id
            )
            try:
                user = session.exec(
                    query
                ).one()  # Possível erro de usuário não encontrado
                session.delete(user)
                session.commit()
                response.data_type = "user_deleted"
                self.tiny_engine.table("player").remove(doc_ids=[user_id])
                response.message = f"user {user_id} has been deleted"
            except Exception as e:
                print(__file__, e, "\nusername not found")

        return response

    def createDefaultPlayerStats(self, player_id):
        newPlayer = Player(id=player_id)
        self.tiny_engine.table("player").insert(newPlayer.__dict__)

    def getPlayerById(self, player_id):
        res = self.tiny_engine.table("player").get(doc_id=player_id)
        return res

    def authUser(self, username: str, password: str):
        response = APIResponseProps(message="username or password invalid")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.username == username.lower()
            )
            try:
                user = session.exec(
                    query
                ).one()  # Possível erro de usuário não encontrado
                results = user.model_dump()
                assert security.verify(
                    password, results["password"]
                )  # Possível erro de senha inválida
                results["created_at"] = str(results["created_at"])
                results["last_login"] = str(results["last_login"])
                # remove password data
                results.pop("password")

                response.data_type = "user_data"
                response.message = f"{username} has authentication successful"
                response.user_data = results
                print(response.message)
                user.onLogin()
                session.add(user)
                session.commit()

            except Exception as e:
                print(__file__, e, "\nusername or password invalid")

        return response

    def getUserDataById(self, user_id: int):
        response = APIResponseProps(message=f"user with id {user_id} not found")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.id == user_id
            )
            try:
                user = session.exec(
                    query
                ).one()  # Possível erro de usuário não encontrado
                results = user.model_dump()
                results["created_at"] = str(results["created_at"])
                results["last_login"] = str(results["last_login"])
                # remove password data
                results.pop("password")

                response.data_type = "user_data"
                response.message = "User data"
                response.user_data = results

            except:
                print(__file__, "\nusername not found")

        return response


DB = DB_Manager()
