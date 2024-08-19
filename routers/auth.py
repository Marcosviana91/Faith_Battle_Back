# from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

# from fastapi.security import OAuth2PasswordRequestForm
from schemas.users_schema import AuthSchema, UserWs
from utils.ConnectionManager import WS
from utils.DataBaseManager import DB
from utils.security import createAccessToken
from utils.LoggerManager import Logger

router = APIRouter(prefix="/auth", tags=["auth"])

# T_OAuth2Form = Annotated[AuthSchema, Depends()]


@router.post("/token")
def handleAuth(form_data: AuthSchema):
    db_response = DB.authUser(
        username=form_data.username,
        password=form_data.password,
    )
    if db_response.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=db_response.message
        )
    access_token = createAccessToken({
        "sub": db_response.user_data.get("id"),
    })
    res = {"access_token": access_token, "token_type": "Bearer", "sub": db_response.user_data.get("id")}
    authenticated_user = UserWs(
        id=db_response.user_data.get("id"),
        token=access_token
    )
    Logger.info(f'user id {db_response.user_data.get("id")} authenticated successfully', 'AUTH')
    WS.login(authenticated_user)
    return res
