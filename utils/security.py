from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError
from passlib.hash import argon2
from zoneinfo import ZoneInfo, available_timezones

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def encrypt(password: str):
    return argon2.hash(password)


def verify(password: str, encrypted_password: str):
    return argon2.verify(password, encrypted_password)


def createAccessToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("America/Sao_Paulo")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def getCurrentUserAuthenticated(token: str = Depends(oauth2_scheme)):
    # possível erro de token expirado: jwt.exceptions.ExpiredSignatureError
    try:
        payload: dict = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as e:
        print(__file__, e, "\nToken expirado")
    username: str = payload.get("sub")
    return username
