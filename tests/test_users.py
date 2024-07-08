from http import HTTPStatus

from fast_api_zero.schemas import UserPublic


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


def test_read_users(client, token, user):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "username_teste",
                "email": "teste@example.com",
            }
        ]
    }


def test_read_user_with_user(client, user, token):
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_read_one_user_with_user(client, user):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": user.username,
        "email": user.email,
    }


def test_read_user_not_found(client, user, token):
    response = client.get(
        "/users/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user, token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
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


def test_update_user_not_current_user(client, user, token):
    response = client.put(
        "/users/999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "Marques_Igor_Updated",
            "email": "Email_Updated@example.com",
            "password": "12345",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user(client, user, token):
    response = client.delete(
        "/users/1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_user_not_current_user(client, user, token):
    response = client.delete(
        "/users/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}
