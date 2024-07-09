# from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm

from schemas import AuthSchema, UserWs
from utils.DataBaseManager import DB
from utils.ConnectionManager import WS
from utils.security import createAccessToken

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
        "sub": db_response.user_data.get("username"),
        "inf": db_response.user_data
    })
    res = {"access_token": access_token, "token_type": "Bearer"}
    authenticated_user = UserWs(
        id=db_response.user_data.get("id"),
        token=access_token
    )
    WS.login(authenticated_user)
    return res
