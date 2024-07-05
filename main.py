from secrets import token_hex

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.sessions import SessionMiddleware

from schemas import APIResponseSchema, UserSchema
from utils import DB
from utils.populates import UserPopulate
from utils.security import createAccessToken, getCurrentUserAuthenticated

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
def handleRoot():
    res = JSONResponse(
        content={"message": "Root router ok"}, status_code=status.HTTP_200_OK
    )
    return res


# Create new user
@app.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponseSchema,
)
def handleNewUser(user: UserSchema):
    db_response = DB.createNewUser(user)
    if db_response.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=db_response.message
        )
    return db_response


@app.get(
    "/user/{user_id}",
    response_model=APIResponseSchema,
)
async def getUserDataById(
    user_id: int,
):
    db_response = DB.getUserDataById(user_id)
    if db_response.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=db_response.message
        )
    return db_response


@app.post("/auth")
def handleAuth(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = DB.authUser(
        username=form_data.username,
        password=form_data.password,
    )
    if user_data.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=user_data.message
        )
    else:
        access_token = createAccessToken({
            "sub": user_data.user_data.get("username")
        })
        res = {"access_token": access_token, "token_type": "Bearer"}
        return res


@app.put(
    "/user/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=APIResponseSchema,
)
def updateUserData(
    user_id: int,
    user_new_data: UserSchema,
    current_user_authenticated=Depends(getCurrentUserAuthenticated),
):
    __user = DB.getUserDataById(user_id)

    # print(__user.user_data.get('username'))
    # print(user_new_data)
    # print(current_user_authenticated)

    if current_user_authenticated != __user.user_data.get("username"):
        print("Não pode alterar")
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=(
                "You must have admin previlegies to change other user's data"
            ),
        )
    print("Pode alterar")
    db_response = DB.updateUser(user_id, user_new_data)
    return db_response
