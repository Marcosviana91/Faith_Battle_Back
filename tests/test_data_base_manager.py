from schemas import NewUserSchema
from utils.DataBaseManager import DB


def test_createNewUser_ok():
    user_data = NewUserSchema(**{
        "username": "usuario_de_test",
        "password": "123asd",
        "real_name": "Eu Sou Um Test",
        "email": "usuario_test@email.co",
    })
    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "user_created"


def test_createNewUser_error_username_already_exist():
    user_data = NewUserSchema(**{
        "username": "usuario_de_test",
        "password": "123asd",
        "real_name": "Eu Sou Um Test",
        "email": "usuario_test@email.co",
    })

    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "error"


def test_createNewUser_error_email_already_exist():
    user_data = NewUserSchema(**{
        "username": "usuario_de_test2",
        "password": "123asd",
        "real_name": "Eu Sou Um Test",
        "email": "usuario_test@email.co",
    })

    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "error"


def test_updateUser_ok():
    user_id = 1
    user_data = NewUserSchema(**{
        "username": "usuario_de_test_atualizado",
        "password": "123asd",
        "real_name": "Eu Sou Um Test Atualizado",
        "email": "usuario_test_atualizado@email.co",
    })
    db_response = DB.updateUser(user_id, user_data)
    assert db_response.data_type == "user_updated"


def test_updateUser_error():
    user_data = {
        "username": "usuario_de_test2",
        "password": "123asd",
        "real_name": "Eu Sou Um Test",
        "email": "usuario_test@email.co",
    }
    db_response = DB.updateUser(22, user_data)
    assert db_response.data_type == "error"


def test_get_player_by_id():
    user_id = 1
    db_response = DB.getPlayerById(user_id)
    assert db_response.get("id") == user_id


def test_get_user_data_by_id_ok():
    user_id = 1
    db_response = DB.getUserDataById(user_id)
    assert db_response.data_type == "user_data"
    assert db_response.user_data.get("username") == "usuario_de_test_atualizado"


def test_get_user_data_by_id_error():
    user_id = 2
    db_response = DB.getUserDataById(user_id)
    assert db_response.data_type == "error"


def test_auth_user_ok():
    username = "usuario_de_test_atualizado"
    password = "123asd"
    db_response = DB.authUser(username, password)
    assert db_response.data_type == "user_data"


def test_auth_user_error():
    username = "usuario_de_test_atualizado"
    password = "123asd__"
    db_response = DB.authUser(username, password)
    assert db_response.data_type == "error"


def test_deleteUser_ok():
    user_id = 1
    db_response = DB.deleteUser(user_id)
    assert db_response.data_type == "user_deleted"
    assert db_response.message == f"user {user_id} has been deleted"


def test_deleteUser_error():
    user_id = 2
    db_response = DB.deleteUser(user_id)
    assert db_response.data_type == "error"
