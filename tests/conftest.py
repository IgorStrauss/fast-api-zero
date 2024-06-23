import pytest
from fastapi.testclient import TestClient

from fast_api_zero.app import app


@pytest.fixture()
def client():
    """Definindo cliente de testes"""
    return TestClient(app)
