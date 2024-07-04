from sqlmodel import Session, SQLModel, create_engine, select
from tinydb import TinyDB

import models
from schemas import APIResponseProps, Player
from utils import security


class DB_Manager:
    """
    Handle the data persistance
    """

    def __init__(self):
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///database/{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=False)
        SQLModel.metadata.create_all(self.engine)
        tinydb_file_name = "database.json"
        self.tiny_engine = TinyDB(f"./database/{tinydb_file_name}")

    def createNewUser(self, data) -> APIResponseProps:
        response = APIResponseProps("user not created")
        newUser = models.UserModel(**data)
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
                newUser.password = security.encrypt(data["password"])
                session.add(newUser)
                session.commit()

                self.createDefaultPlayerStats(player_id=newUser.id)
                response.data_type = "user_created"
                response.message = "user successful created"

        return response

    def updateUser(self, user_name, data) -> APIResponseProps:
        response = APIResponseProps("user not updated")
        userUpdated = models.UserModel(**data)
        with Session(self.engine) as session:
            query_username = select(models.UserModel).where(
                models.UserModel.username == user_name
            )
            try:
                user = session.exec(
                    query_username
                ).one()  # Possível erro de usuário não encontrado

                user.email = userUpdated.email
                user.real_name = userUpdated.real_name
                user.username = userUpdated.username
                user.password = security.encrypt(userUpdated.password)

                session.add(user)
                session.commit()
                response.data_type = "user_updated"
                response.message = "user has been updated"
            except Exception as e:
                response.message = e
                print(e)
        return response

    def deleteUser(self, user_name) -> APIResponseProps:
        response = APIResponseProps(message="username not found")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.username == user_name
            )
            try:
                user = session.exec(
                    query
                ).one()  # Possível erro de usuário não encontrado
                session.delete(user)
                session.commit()
                response.data_type = "user_deleted"
                response.message = f"user {user.username} has been deleted"
            except:
                print(__file__, "\nusername not found")

        return response

    def createDefaultPlayerStats(self, player_id):
        newPlayer = Player(id=player_id)
        self.tiny_engine.table("player").insert(newPlayer.__dict__)

    def getPlayerById(self, player_id):
        res = self.tiny_engine.table("player").get(doc_id=player_id)
        return res

    def authUser(self, username, password):
        response = APIResponseProps(message="username or password invalid")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.username == username
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
                response.message = "authentication successful"
                response.user_data = results
                print("authentication successful")
                user.onLogin()
                session.add(user)
                session.commit()

            except:
                print(__file__, "\nusername or password invalid")

        return response

    def getUserData(self, username: str):
        response = APIResponseProps(message="username not found")
        with Session(self.engine) as session:
            query = select(models.UserModel).where(
                models.UserModel.username == username
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
