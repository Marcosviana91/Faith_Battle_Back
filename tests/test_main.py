from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_handleRoot_deve_retornar_message_Root_router_ok():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Root router ok"}


def test_get_token():
    response = client.post(
        "/auth",
        data={"username": "p0", "password": "p0"},
    )
    token = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
