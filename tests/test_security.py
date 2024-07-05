from jwt import decode

from utils.security import (
    createAccessToken,
    env_settings,
)


def test_jwt():
    data = {"sub": "test@test.com"}
    token = createAccessToken(data)

    result = decode(
        token, env_settings.SECRET_KEY, algorithms=[env_settings.ALGORITHM]
    )

    assert result["sub"] == data["sub"]
    assert result["exp"]
