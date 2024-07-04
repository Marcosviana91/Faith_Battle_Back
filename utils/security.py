from datetime import datetime, timedelta

from jwt import encode
from passlib.hash import argon2
from zoneinfo import ZoneInfo

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def encrypt(password: str):
    return argon2.hash(password)


def verify(password: str, encrypted_password: str):
    return argon2.verify(password, encrypted_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt
