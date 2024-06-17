from utils.DataBaseManager import DB_Manager

from models import User

fake_users = [
    ('p0', 'p0', 'p0', '00@email.com'),
    ('p1', 'p1', 'p1', '01@email.com'),
    ('p2', 'p2', 'p2', '02@email.com'),
    ('p3', 'p3', 'p3', '03@email.com'),
    ('p4', 'p4', 'p4', '04@email.com'),
    ('p5', 'p5', 'p5', '05@email.com'),
    ('p6', 'p6', 'p6', '06@email.com'),
    ('p7', 'p7', 'p7', '07@email.com'),
    ('p8', 'p8', 'p8', '08@email.com'),
    ('p9', 'p9', 'p9', '09@email.com'),

]

DB = DB_Manager()

for user in fake_users:
    newUser = User(*user
    )
    print(DB.createNewUser(newUser.model_dump())['message'])