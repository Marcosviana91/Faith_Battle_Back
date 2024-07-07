from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, room, users
from settings import env_settings

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(room.router)

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
    res = {"message": "Root router ok"}
    return res


@app.get("/populate")
def handlePopulate():
    from utils.populates import UserPopulate

    res = {"message": "Populated"}
    return res
