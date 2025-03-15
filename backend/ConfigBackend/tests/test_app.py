from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app import app


def test_health_must_return_healthy():
    client = TestClient(app)

    response = client.get('/health')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'healthy'}
