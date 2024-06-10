from utils.DataBaseManager import DB_Manager

from models import User

fake_users = [
    ('marcox00', '123asd', 'Marcos Viana', 'marcos@email.com'),
    ('akio', '123qwe', 'Fernando Jefté', 'jefte@teste.com'),
    ('akio_mana', '123zxc', 'Débora França', 'deb@email.com'),
]

DB = DB_Manager()

for user in fake_users:
    newUser = User(*user
    )
    print(DB.createNewUser(newUser.model_dump())['message'])