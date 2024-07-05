# from jwt import decode

# from utils.security import (
#     ALGORITHM,
#     SECRET_KEY,
#     createAccessToken,
# )


# def test_jwt():
#     data = {"sub": "test@test.com"}
#     token = createAccessToken(data)

#     result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#     assert result["sub"] == data["sub"]
#     assert result["exp"]
