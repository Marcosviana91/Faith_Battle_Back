from pprint import pprint
from typing import Annotated

from fastapi import FastAPI, Body, status
from fastapi.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from secrets import token_hex

from utils import WS_Manager, DB_Manager

# from utils.populates import CardPopulate, UserPopulate

import json


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
DB = DB_Manager()


@app.get('/api')
def handleRoot(req: Request):
    crfs_token = token_hex(8)
    # print("headers: ", req.headers)
    # print("cookies: ", req.cookies)
    # print("session: ", req.session)
    # print("method: ", req.method)
    # print("path_params: ", req.path_params)
    # print("query_params: ", req.query_params)
    res = HTMLResponse(content='API')
    # res.set_cookie("crfs_token", crfs_token)
    # res.delete_cookie("crfs")
    return res


@app.post('/auth')
async def handleAuth(req: Request):
    data = json.loads(await req.body())
    # print(data)
    print("session: ", req.session)

    user_data = DB.authUser(username=data["username"], password=data["password"])
    # print(user_data)

    # crfs_token = token_hex(8)
    # req.session['auth'] = crfs_token
    req.session['user_info'] = user_data['data']

    res = JSONResponse(content=user_data, status_code=status.HTTP_202_ACCEPTED)

    # res.set_cookie("user_info", user_data)
    # res.delete_cookie("user_info")
    return res

@app.post('/newuser')
async def handleNewUser(req: Request):
    data = json.loads(await req.body())
    user_data = DB.createNewUser(data)
    res = JSONResponse(content=user_data, status_code=status.HTTP_201_CREATED)
    
    return res


@app.websocket('/websocket_conn')
def handleWebSockets(req: Request):
    pass
