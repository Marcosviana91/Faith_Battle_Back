import requests
from fastapi import APIRouter, HTTPException

from settings import env_settings as env

from schemas.users_schema import AuthSchema
from utils.ConnectionManager import WS
from utils.LoggerManager import Logger

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
def handleAuth(form_data: AuthSchema):
    if form_data.username and form_data.password:
        auth = requests.post(f'http://{env.DB_HOST}:3111/api/auth',
                             json={'username': form_data.username.lower(), 'password': form_data.password})
        print(auth.status_code)
        if auth.status_code == 200:
            Logger.info(f'user {form_data.username} authenticated successfully', 'AUTH')
            Logger.status(f'authenticated successfully: {auth.json()} ', 'AUTH')
            return auth.json()
        else:
            print(auth.status_code)
            print(auth.text)
    return HTTPException(detail=auth.text, status_code=auth.status_code)
