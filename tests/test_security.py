from jwt import decode

from fast_api_zero.security import create_access_token, settings


def test_jwt():
    data = {"sub": "test@email.com"}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY,
                     algorithms=[settings.ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]
