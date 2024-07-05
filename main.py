from secrets import token_hex

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from routers import auth, users

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)

secret_key = token_hex()

app.add_middleware(SessionMiddleware, secret_key=secret_key)
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
def handleRoot():
    from utils.populates import UserPopulate
    res = {"message": "Populated"}
    return res


