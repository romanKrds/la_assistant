import pytest
from la_assistant import create_app
from la_assistant.extensions import db as _db
from data import populate_users, populate_user_vocabulary, populate_vocabulary


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # using in-memory SQLite for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    # create the database and load test data
    with app.app_context():
        _db.create_all()
        populate_users(_db)
        populate_user_vocabulary(_db)
        populate_vocabulary(_db)

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            json={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
