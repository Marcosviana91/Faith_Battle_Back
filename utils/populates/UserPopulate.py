from schemas.users_schema import NewUserSchema
from utils.DataBaseManager import DB

# username, password, real_name, e-mail
fake_users = [
    {
        "username": "P0",
        "password": "p0",
        "real_name": "p0",
        "avatar": 0,
        # "email": "p0@email.co",
    },
    {
        "username": "p1",
        "password": "p1",
        "real_name": "p1",
        "avatar": 1,
        # "email": "p1@email.co",
    },
    {
        "username": "p2",
        "password": "p2",
        "real_name": "p2",
        "avatar": 2,
        # "email": "p2@email.co",
    },
    {
        "username": "p3",
        "password": "p3",
        "real_name": "p3",
        "avatar": 3,
        # "email": "p3@email.co",
    },
    {
        "username": "p4",
        "password": "p4",
        "real_name": "p4",
        "avatar": 4,
        # "email": "p4@email.co",
    },
    {
        "username": "p5",
        "password": "p5",
        "real_name": "p5",
        "avatar": 5,
        # "email": "p5@email.co",
    },
    {
        "username": "p6",
        "password": "p6",
        "real_name": "p6",
        "avatar": 6,
        # "email": "p6@email.co",
    },
    {
        "username": "p7",
        "password": "p7",
        "real_name": "p7",
        "avatar": 7,
        # "email": "p7@email.co",
    },
    {
        "username": "p8",
        "password": "p8",
        "real_name": "p8",
        "avatar": 8,
        # "email": "p8@email.co",
    },
    {
        "username": "p9",
        "password": "p9",
        "real_name": "p9",
        "avatar": 9,
        # "email": "p9@email.co",
    },
]


for user in fake_users:
    newUser = NewUserSchema(**user)
    DB.createNewUser(newUser)
