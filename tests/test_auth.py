import pytest
from flask import g, session
from la_assistant.db import get_db


def test_register(client, app):
    response = client.post('/auth/register', json={'username': 'a', 'password': 'a'})
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', 'Username is required.'),
    ('a', '', 'Password is required.'),
    ('test', 'test', 'User test is already registered.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        json={'username': username, 'password': password}
    )
    assert message in response.json.get('error')


def test_login(client, auth):
    auth.login()

    with client:
        client.get('/')
        assert g.user['username'] == 'test'
        assert session['token'] is not None
        assert session['token'] == g.user['token']


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', 'test', 'Username is required.'),
    ('a', '', 'Password is required.'),
    ('a', 'test', 'Incorrect username.'),
    ('test', 'a', 'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.json.get('error')


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'token' not in session