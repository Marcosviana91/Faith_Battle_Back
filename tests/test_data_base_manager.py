from utils import DB


def test_createNewUser_ok():
    user_data = {
        "username": "marcosviana91",
        "password": "123asd",
        "real_name": "Marcos Antônio Gonzaga Viana",
        "email": "marcos.viana.91@gmail.com",
    }

    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "user_created"


def test_createNewUser_error_username_already_exist():
    user_data = {
        "username": "marcosviana91",
        "password": "123asd",
        "real_name": "Marcos Antônio Gonzaga Viana",
        "email": "marcos.viana.91@gmail.com",
    }

    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "error"


def test_createNewUser_error_email_already_exist():
    user_data = {
        "username": "marcosviana912",
        "password": "123asd",
        "real_name": "Marcos Antônio Gonzaga Viana",
        "email": "marcos.viana.91@gmail.com",
    }

    db_response = DB.createNewUser(user_data)
    assert db_response.data_type == "error"


def test_updateUser_ok():
    user_data = {
        "username": "marcosviana912",
        "password": "123asd",
        "real_name": "Marcos Antônio Gonzaga Viana",
        "email": "marcos.viana.91@gmail.com",
    }
    db_response = DB.updateUser("marcosviana91", user_data)
    assert db_response.data_type == "user_updated"


def test_updateUser_error():
    user_data = {
        "username": "marcosviana912",
        "password": "123asd",
        "real_name": "Marcos Antônio Gonzaga Viana",
        "email": "marcos.viana.91@gmail.com",
    }
    db_response = DB.updateUser("marcosviana913", user_data)
    assert db_response.data_type == "error"


def test_deleteUser_ok():
    db_response = DB.deleteUser("marcosviana912")
    assert db_response.data_type == "user_deleted"


def test_deleteUser_error():
    db_response = DB.deleteUser("marcosviana913")
    assert db_response.data_type == "error"
