from jwt import decode
from jwt.exceptions import ExpiredSignatureError

from settings import env_settings


def getCurrentUserAuthenticated(token: str):
    # possível erro de token expirado: jwt.exceptions.ExpiredSignatureError
    try:
        payload: dict = decode(
            token, env_settings.SECRET_KEY, algorithms=[env_settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        return username
    except ExpiredSignatureError as e:
        print(__file__, e, "\tToken expirado")
