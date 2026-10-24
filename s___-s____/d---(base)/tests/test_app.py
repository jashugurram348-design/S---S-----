
import pytest

from __init__ import create_app
from database import db


@pytest.fixture
def app():
    """Create a separate test application and database."""
    app = create_app()

    app.config.update(
        TESTING=True,
        DEBUG=False,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_ENGINE_OPTIONS={
            "connect_args": {"check_same_thread": False}
        },
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()


def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["app"] == "SignSpeak API"


def test_health_route(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_api_status(client):
    response = client.get("/api/status")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["status"] == "running"


def test_translate_hello(client):
    response = client.post(
        "/api/translate/",
        json={"text": "hello", "mode": "text"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["translated_text"] == "Hello"


def test_translate_empty_text(client):
    response = client.post(
        "/api/translate/",
        json={"text": "", "mode": "text"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_translate_invalid_mode(client):
    response = client.post(
        "/api/translate/",
        json={"text": "hello", "mode": "invalid"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_unknown_route(client):
    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    assert response.get_json()["success"] is False
