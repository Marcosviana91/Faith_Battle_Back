from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, room, users, websocket
from settings import env_settings
from utils.MatchManager import MATCHES

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
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def handleRoot():
    res = {"message": "Root router ok"}
    return res


@app.get("/populate")
def handlePopulate():
    from utils.populates import UserPopulate
    res = {"message": "Populated"}
    return res

@app.get("/fake_match")
async def makeFakeMatch():
    from utils.populates import FakeMatch
    await FakeMatch.createFakeMatch()
    res = {"message": "fake_match"}
    return res


@app.get("/get_match_stats")
async def getFakeMatch():
    res = MATCHES.getStats
    return res

