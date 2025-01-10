import os
import sys

import pytest
import fakeredis
from backend.app import create_app
from backend.app.models.data import Post, PostComment, Settings, Thesis, User #, TokenBlacklist

from ..utils.db import database_proxy

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


@pytest.fixture
def app():
    """
    Set up the Flask app with testing configuration.
    """
    app = create_app("testing")

    # Initialize the SQLite test database
    with app.app_context():
        database_proxy.connect()
        database_proxy.create_tables([Post, PostComment, Settings, Thesis, User], safe=True)
        yield app
        database_proxy.drop_tables([Post, PostComment, Settings, Thesis, User])
        database_proxy.close()

@pytest.fixture(scope="function", autouse=True)
def mock_redis(monkeypatch):
    """
    Mock Redis for all tests using fakeredis with function scope.
    """
    redis_mock = fakeredis.FakeStrictRedis()

    # Replace the get_redis_client function for the duration of each test
    def mock_get_redis_client():
        return redis_mock

    monkeypatch.setattr("backend.app.utils.redis_helper.get_redis_client", mock_get_redis_client)

    yield redis_mock
    redis_mock.flushall()  # Clean up after each test


@pytest.fixture
def client(app):
    """
    Provide a test client for the app.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Provide a test runner for the app.
    """
    return app.test_cli_runner()
