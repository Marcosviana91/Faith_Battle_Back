import requests

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, room, users, websocket
from settings import env_settings

from utils.Cards.standard.raw_data import STANDARD_CARDS

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(room.router)
app.include_router(websocket.router)

app.add_middleware(SessionMiddleware, secret_key=env_settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
    # exposed_headers= HEADERS,
)
@app.get("/")
def handleRoot():
    server_settings = requests.get(f'http://{env_settings.API_HOST}:3111/api/')
    res = {
        'version': 'alpha-1.1.1',
        'active_cards': STANDARD_CARDS
    }
    if server_settings.status_code == 200:
        res.update(server_settings.json())
    return res


