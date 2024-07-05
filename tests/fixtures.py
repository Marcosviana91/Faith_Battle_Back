import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture()
def getToken():
    response = client.post("/auth", data={"username": "p0", "password": "p0"})
    return response.json()["access_token"]
