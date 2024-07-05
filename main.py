from secrets import token_hex

<<<<<<< HEAD
# from utils import DB
# from utils.populates import UserPopulate

import json
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
>>>>>>> only_auth

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


<<<<<<< HEAD
@app.get('/')
async def handleRoot(req: Request):
    res = JSONResponse(content={"message": "Root router ok"},
                           status_code=status.HTTP_200_OK)
    return res

# @app.post('/auth')
# async def handleAuth(req: Request):
#     data: dict = json.loads(await req.body())
#     user_data = DB.authUser(
#         username=data.get("username"),
#         password=data.get("password"),
#     )
#     if user_data.data_type == 'error':
#         res = JSONResponse(content=user_data.__dict__,
#                            status_code=status.HTTP_401_UNAUTHORIZED)
#     else:
#         req.session['user_info'] = user_data.user_data
#         print("session: ", req.session)
#         res = JSONResponse(content=user_data.__dict__,
#                            status_code=status.HTTP_202_ACCEPTED)
#     return res


# @app.post('/newuser')
# async def handleNewUser(req: Request):
#     data = json.loads(await req.body())
#     user_data = DB.createNewUser(data)
#     res = JSONResponse(content=user_data.__dict__, status_code=status.HTTP_201_CREATED)
#     return res
=======
@app.get("/")
def handleRoot():
    res = {"message": "Root router ok"}
    return res


@app.get("/populate")
def handlePopulate():
    from utils.populates import UserPopulate

    res = {"message": "Populated"}
    return res
>>>>>>> only_auth
