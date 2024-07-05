from fastapi import Depends, status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def getToken():
    response = client.post(
        "/auth", data={"username": "usuario_de_test", "password": "123asd"}
    )
    return response.json()["access_token"]


def test_handleRoot_deve_retornar_message_Root_router_ok():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Root router ok"}


def test_create_new_user_ok():
    response = client.post(
        "/user",
        json={
            "username": "usuario_de_test",
            "password": "123asd",
            "real_name": "Eu Sou Um Test",
            "email": "usuario_test@email.co",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_new_user_error():
    response = client.post(
        "/user",
        json={
            "username": "usuario_de_test",
            "password": "123asd",
            "real_name": "Eu Sou Um Test",
            "email": "usuario_test@email.co",
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_get_user_data_ok():
    user_id = 11
    response = client.get(f"/user/{user_id}")
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["user_data"]["id"] == user_id


def test_get_user_data_error():
    user_id = 21
    response = client.get(f"/user/{user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_auth_ok():
    response = client.post(
        "/auth",
        data={"username": "p0", "password": "p0"},
    )
    token = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token


def test_auth_error():
    response = client.post(
        "/auth",
        data={"username": "p0", "password": "p1"},
    )
    token: dict = response.json()
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert token.get("detail") == "username or password invalid"


def test_user_update_ok():
    token = getToken()
    user_id = 11
    response = client.put(
        f"/user/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "usuario_de_test",
            "password": "__not-change__",
            "real_name": "Eu Sou Um Test Atualizado",
            "email": "usuario_test_atualizado@email.co",
        },
    )
    print(response.json())
    assert response.status_code == status.HTTP_202_ACCEPTED


def test_user_update_error():
    token = getToken()
    user_id = 21
    response = client.put(
        f"/user/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "usuario_de_test",
            "password": "__not-change__",
            "real_name": "Eu Sou Um Test Atualizado",
            "email": "usuario_test_atualizado@email.co",
        },
    )
    print(response.json())
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
