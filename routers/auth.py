from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from utils.DataBaseManager import DB
from utils.security import createAccessToken

router = APIRouter(prefix="/auth", tags=["auth"])

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post("/token")
def handleAuth(form_data: T_OAuth2Form):
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
            "sub": user_data.user_data.get("username"),
            "inf": user_data.user_data
        })
        res = {"access_token": access_token, "token_type": "Bearer"}
        return res
