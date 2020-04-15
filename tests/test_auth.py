"""Auth test script."""

import pytest
from flask import session, g
from flaskr.db import get_db


def test_register(client, app):
    """Valid registration test."""
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered.')
))
def test_register_valid_input(client, username, password, message):
    """Registration validation check."""
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    """Login test."""
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.')
))
def test_login_validate_input(auth, username, password, message):
    """Login validation check."""
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """Logout test."""
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
