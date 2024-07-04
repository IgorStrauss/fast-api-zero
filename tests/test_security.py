from jwt import decode

from fast_api_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {"sub": "test@email.com"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]
