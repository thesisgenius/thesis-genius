import inspect
import os
import sys
from datetime import datetime, timedelta, timezone

import fakeredis
import pytest
from app import create_app
from app.models import data
from app.services.dbservice import DBService
from app.utils.db import database_proxy
from peewee import Model

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
        database_models = [
            cls
            for _, cls in inspect.getmembers(
                data,
                lambda m: isinstance(m, type) and issubclass(m, Model) and m != Model,
            )
        ]
        database_proxy.create_tables(database_models, safe=True)

        yield app
        # Dynamically retrieve all models from data.py
        database_models = [
            model
            for model in data.__dict__.values()
            if isinstance(model, type)
            and issubclass(model, data.BaseModel)
            and model is not data.BaseModel
        ]
        existing_tables = database_proxy.get_tables()

        # Drop only tables that exist
        tables_to_drop = [
            model
            for model in database_models
            if model._meta.table_name in existing_tables
        ]
        if tables_to_drop:
            database_proxy.drop_tables(tables_to_drop, safe=True)
        database_proxy.close()


@pytest.fixture
def db_service(app):
    """
    Provide a DBService instance for testing.
    """
    return DBService(app)


@pytest.fixture(scope="function", autouse=True)
def mock_redis(monkeypatch):
    redis_mock = fakeredis.FakeStrictRedis()

    def mock_get_redis_client():
        return redis_mock

    def mock_blacklist_token(token, ttl=3600):
        redis_mock.setex(f"blacklist:{token}", ttl, "true")

    def mock_is_token_blacklisted(token):
        return redis_mock.exists(f"blacklist:{token}") > 0

    def mock_add_token_to_user(user_id, token, expiry_seconds):
        token_key = f"user:{user_id}:tokens"
        expiry_time = (
            datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
        ).timestamp()
        redis_mock.hset(token_key, token, str(expiry_time))
        redis_mock.expire(token_key, expiry_seconds)

    def mock_get_user_tokens(user_id):
        token_key = f"user:{user_id}:tokens"
        return redis_mock.hgetall(token_key)

    def mock_revoke_user_tokens(user_id):
        """
        Mock revoking all tokens for a user by blacklisting them.
        """
        token_key = f"user:{user_id}:tokens"
        tokens = redis_mock.hkeys(token_key)

        for token in tokens:
            # Decode token and expiry values (if needed)
            token_str = token if isinstance(token, str) else token.decode("utf-8")
            expiry = redis_mock.hget(token_key, token_str)
            expiry = (
                float(expiry)
                if isinstance(expiry, str)
                else float(expiry.decode("utf-8"))
            )

            # Calculate remaining TTL
            remaining_ttl = max(0, int(expiry - datetime.now(timezone.utc).timestamp()))
            redis_mock.setex(f"blacklist:{token_str}", remaining_ttl, "true")

        # Delete user's token list
        redis_mock.delete(token_key)

    def mock_is_token_expired(token):
        """
        Mock checking if a token is expired based on its tracked expiry.
        """
        expiry_key = f"token:{token}:expiry"
        expiry_timestamp = redis_mock.get(expiry_key)

        if expiry_timestamp is None:  # Key doesn't exist
            return True

        # Ensure expiry_timestamp is handled as a float
        return datetime.now(timezone.utc).timestamp() > float(expiry_timestamp)

    monkeypatch.setattr(
        "app.utils.redis_helper.get_redis_client", mock_get_redis_client
    )
    monkeypatch.setattr("app.utils.redis_helper.blacklist_token", mock_blacklist_token)
    monkeypatch.setattr(
        "app.utils.redis_helper.is_token_blacklisted", mock_is_token_blacklisted
    )
    monkeypatch.setattr(
        "app.utils.redis_helper.add_token_to_user", mock_add_token_to_user
    )
    monkeypatch.setattr("app.utils.redis_helper.get_user_tokens", mock_get_user_tokens)
    monkeypatch.setattr(
        "app.utils.redis_helper.revoke_user_tokens", mock_revoke_user_tokens
    )
    monkeypatch.setattr(
        "app.utils.redis_helper.is_token_expired", mock_is_token_expired
    )

    yield redis_mock
    redis_mock.flushall()


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


@pytest.fixture
def create_role():
    """
    Fixture to create default roles in the database.
    """
    for role_name in ["Student", "Teacher", "Admin"]:
        data.Role.get_or_create(name=role_name)


@pytest.fixture
def user_token(client, create_role):
    """
    Fixture to register and log in a user, returning the JWT token.
    """
    client.post(
        "/api/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "institution": "National University",
            "username": "testuser",
            "password": "password123",
            "role": "Student",
        },
    )
    login_response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json["token"]
    assert token is not None
    return token
