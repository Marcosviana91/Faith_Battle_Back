import json
from secrets import token_hex

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.sessions import SessionMiddleware

from utils import DB
from utils.security import create_access_token

ORIGINS = ["*"]
METHODS = ["*"]
HEADERS = ["*"]

app = FastAPI()

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
async def handleRoot(req: Request):
    res = JSONResponse(
        content={"message": "Root router ok"}, status_code=status.HTTP_200_OK
    )
    return res


@app.post("/auth")
async def handleAuth(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = DB.authUser(
        username=form_data.username,
        password=form_data.password,
    )
    if user_data.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=user_data.message
        )
    else:
        access_token = create_access_token({
            "sub": user_data.user_data.get("email")
        })
        # res = JSONResponse(
        #     content=user_data.__dict__, status_code=status.HTTP_202_ACCEPTED
        # )
        res = {"access_token": access_token, "token_type": "Bearer"}
        return res


@app.post("/newuser")
async def handleNewUser(req: Request):
    data = json.loads(await req.body())
    user_data = DB.createNewUser(data)
    res = JSONResponse(
        content=user_data.__dict__, status_code=status.HTTP_201_CREATED
    )
    return res
