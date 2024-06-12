from sqlmodel import Session, SQLModel, create_engine, select
from tinydb import TinyDB, Query

from utils import hash_pass
import models


class DB_Manager:
    '''
    Handle the data persistance
    '''
    def __init__(self):
        sqlite_file_name = "database.db"
        sqlite_url = f"sqlite:///database/{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=False)
        SQLModel.metadata.create_all(self.engine)
        tinydb_file_name = "database.json"
        self.tiny_engine = TinyDB(f'./database/{tinydb_file_name}')
        

    def createNewUser(self, data):
        response = {
            "type": '',
            "message": '',
            "data": {},
        }
        newUser = models.User(**data)
        newUser.password = hash_pass.encrypt(data['password'])
        
        with Session(self.engine) as session:
            query = (
                select(models.User)
                .where(models.User.username == newUser.username)
            )
            check_username = session.exec(query)
            
            query = (
                select(models.User)
                .where(models.User.email == newUser.email)
            )
            check_email = session.exec(query)
            
            if (len( check_username.all()) > 0):
                # print("username already exists")
                response['type'] = 'error'
                response['message'] = 'username already exists'

            if (len( check_email.all()) > 0):
                # print("email already in use")
                response['type'] = 'error'
                if (response['message'] == 'username already exists'):
                    response['message'] = 'username already exists\nemail already in use'
                else:
                    response['message'] = 'email already in use'
                
            else:
                # print("user successful created")
                session.add(newUser)
                session.commit()
                newPlayer = models.Player(id=newUser.id, available_cards=1,decks=1)
                
                response['type'] = 'data'
                response['message'] = 'user successful created'
                response['data'] = {}

        return response

    def authUser(self, username, password):
        response = {
            "type": str,
            "message": str,
            "data": dict,
        }
        with Session(self.engine) as session:
            query = (
                select(models.User)
                .where(models.User.username == username)
            )
            try:
                results = session.exec(query).one()
                results = results.model_dump()
                assert (hash_pass.verify(password, results['password']))
                results['created_at'] = str(results['created_at'])
                results['last_login'] = str(results['last_login'])
                # remove password data
                results.pop('password')
                
                response['type'] = 'data'
                response['message'] = 'authentication successful'
                response["data"] = results
                print("authentication successful")

            except:
                response['type'] = 'error'
                response['message'] = 'Nothing matches'
                response['data'] = {}

        return response
    
    def newRoom(self, data):
        newRoom = models.Match(**data)
        print(newRoom)
        # with Session(self.engine) as session:
        #     session.add(newRoom)
        #     session.commit()
        #     print(newRoom.id)
    