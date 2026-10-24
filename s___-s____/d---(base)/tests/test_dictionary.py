
import pytest

from __init__ import create_app
from database import db


@pytest.fixture
def app():
    """Create a test app with an isolated in-memory database."""
    app = create_app()

    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_ENGINE_OPTIONS={
            "connect_args": {"check_same_thread": False}
        },
    )

    with app.app_context():
        db.create_all()

        # Add sample dictionary records.
        from models import DictionaryEntry

        db.session.add_all([
            DictionaryEntry(
                word="Hello",
                description="A greeting.",
                category="Greetings",
                language="ISL",
            ),
            DictionaryEntry(
                word="Thank you",
                description="An expression of gratitude.",
                category="Common phrases",
                language="ISL",
            ),
        ])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_list_dictionary(client):
    response = client.get("/api/dictionary/")

    assert response.status_code == 200
    data = response.get_json()
    assert data is not None


def test_search_dictionary(client):
    response = client.get("/api/dictionary/?q=hello")

    assert response.status_code == 200
    data = response.get_json()
    assert data is not None


def test_get_dictionary_categories(client):
    response = client.get("/api/dictionary/categories")

    assert response.status_code == 200
    assert response.get_json() is not None


def test_get_dictionary_entry_not_found(client):
    response = client.get("/api/dictionary/999999")

    assert response.status_code == 404


def test_dictionary_response_is_json(client):
    response = client.get("/api/dictionary/")

    assert response.is_json


def test_search_with_no_results(client):
    response = client.get(
        "/api/dictionary/?q=nonexistentword123"
    )

    assert response.status_code == 200
    assert response.get_json() is not None
