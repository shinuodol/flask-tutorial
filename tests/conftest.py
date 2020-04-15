"""Setup functions(fixtures)."""
import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """Initialize app fixture."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Client makes request without running server."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Can call the Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    """Test authentication class methods."""

    def __init__(self, client):
        """Initialization method."""
        self._client = client

    def login(self, username='test', password='test'):
        """Test login call."""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """Test logout call."""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Authentication fixture."""
    return AuthActions(client)
