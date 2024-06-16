from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_api_zero.app import app

client = TestClient(app)


def test_read_root_deve_retornar_ola_mundo():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Message": "Olá Mundo!"}
