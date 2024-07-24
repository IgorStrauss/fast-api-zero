import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_api_zero.app import app
from fast_api_zero.database import get_session
from fast_api_zero.models import User, table_registry
from fast_api_zero.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


# Fixture criada para os testes com containertest postgres
@pytest.fixture(scope="session")
def engine():
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


# Fixture recebe a engine da função anterior, com base nos testes postgres
@pytest.fixture()
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


# @pytest.fixture()
# def session():
#     engine = create_engine(
#         "sqlite:///:memory:",
#         connect_args={"check_same_thread": False},
#         poolclass=StaticPool,
#     )
#     table_registry.metadata.create_all(engine)

#     with Session(engine) as session:
#         yield session

#     table_registry.metadata.drop_all(engine)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    password = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")


@pytest.fixture()
def user(session):
    pwd = "12345"

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture()
def other_user(session):
    pwd = "test12345"
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = "test12345"

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        "/auth/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]
