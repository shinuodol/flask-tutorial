"""Flask factory testing."""

from flaskr import create_app


def test_config():
    """Configuration testing."""
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    """Test /hello url."""
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
