from http import HTTPStatus

from bs4 import BeautifulSoup

from fast_api_zero.schemas import UserPublic


def test_read_root_deve_retornar_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_path_html_titulo_da_pagina_deve_retornar_MarquesIgor(client):
    response = client.get("/path-html")

    assert response.status_code == HTTPStatus.OK

    soup = BeautifulSoup(response.text, "html.parser")

    title_tags = soup.find_all("title")
    assert len(title_tags) == 1
    assert title_tags[0].text == "MarquesIgor"


def test_path_html_deve_retornar_html(client):
    response = client.get("/path-html")

    assert response.status_code == HTTPStatus.OK

    soup = BeautifulSoup(response.text, "html.parser")

    h1_tags = soup.find_all("h1")

    expected_h1_tags = 2

    assert len(h1_tags) == expected_h1_tags

    def normalize_text(text):
        return text.replace("\n", "").replace(" ", "").strip()

    assert normalize_text(h1_tags[0].text) == "MarquesIgor"
    assert normalize_text(h1_tags[1].text) == "CursoFastAPIZerocomDunossauro!"


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "Marques_Igor",
            "email": "Email@example.com",
            "password": "12345",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "Marques_Igor",
        "email": "Email@example.com",
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_user_with_user(client, user):
    response = client.get("/users/")
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_one_user_with_user(client, user):
    response = client.get("/user/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": user.username,
        "email": user.email,
    }


def test_read_user_not_found(client, user):
    response = client.get("/user/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user):
    response = client.put(
        "/user/1",
        json={
            "username": "Marques_Igor_Updated",
            "email": "Email_Updated@example.com",
            "password": "12345",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "Marques_Igor_Updated",
        "email": "Email_Updated@example.com",
    }


def test_update_user_not_found(client, user):
    response = client.put(
        "/user/999",
        json={
            "username": "Marques_Igor_Updated",
            "email": "Email_Updated@example.com",
            "password": "12345",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_user(client, user):
    response = client.delete("/user/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_found(client, user):
    response = client.delete("/user/999")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
