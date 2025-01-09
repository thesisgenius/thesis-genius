import os
import sys

import pytest

from backend.app import create_app
from backend.app.models.data import Post, Thesis, User

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
        database_proxy.create_tables([User, Thesis, Post], safe=True)
        yield app
        database_proxy.drop_tables([User, Thesis, Post])
        database_proxy.close()


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
