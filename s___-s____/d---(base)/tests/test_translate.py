
import pytest

from __init__ import create_app


@pytest.fixture
def client():
    """Create a Flask test client."""
    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_translate_hello(client):
    response = client.post(
        "/api/translate/",
        json={"text": "hello", "mode": "text"},
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["original_text"] == "hello"
    assert data["translated_text"] == "Hello"
    assert data["mode"] == "text"


def test_translate_case_insensitive(client):
    response = client.post(
        "/api/translate/",
        json={"text": "HELLO", "mode": "text"},
    )

    assert response.status_code == 200
    assert response.get_json()["translated_text"] == "Hello"


def test_translate_empty_text(client):
    response = client.post(
        "/api/translate/",
        json={"text": "", "mode": "text"},
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_translate_missing_text(client):
    response = client.post(
        "/api/translate/",
        json={"mode": "text"},
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


def test_translate_default_mode(client):
    response = client.post(
        "/api/translate/",
        json={"text": "hello"},
    )

    assert response.status_code == 200
    assert response.get_json()["mode"] == "text"


def test_translate_unknown_phrase(client):
    phrase = "a phrase not in the demo dictionary"

    response = client.post(
        "/api/translate/",
        json={"text": phrase, "mode": "text"},
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["original_text"] == phrase
    assert data["is_demo"] is True


def test_translate_health(client):
    response = client.get("/api/translate/health")

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["status"] == "running"


def test_translate_non_json_body(client):
    response = client.post(
        "/api/translate/",
        data="not json",
        content_type="text/plain",
    )

    assert response.status_code == 400
    assert response.get_json()["success"] is False
