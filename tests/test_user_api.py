import os
import sys

import jwt
import pytest
from dotenv import load_dotenv
from flask import current_app

from server import db
from server.app import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    load_dotenv()
    os.environ["FLASK_ENV"] = "testing"  # Ensure the app uses the testing config
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        yield client


def test_register_user(client):
    """Test registering a new user."""
    response = client.post(
        "/v1/api/users/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"


def test_register_duplicate_user(client):
    """Test registering a duplicate user."""
    # Register the first user
    client.post(
        "/v1/api/users/register",
        json={"email": "duplicate@example.com", "password": "password123"},
    )

    # Attempt to register the same user again
    response = client.post(
        "/v1/api/users/register",
        json={"email": "duplicate@example.com", "password": "password123"},
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_login_user(client):
    """Test logging in with valid credentials."""
    # First, register a user
    client.post(
        "/v1/api/users/register",
        json={"email": "login@example.com", "password": "password123"},
    )

    # Attempt to log in
    response = client.post(
        "/v1/api/users/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_invalid_user(client):
    """Test logging in with invalid credentials."""
    response = client.post(
        "/v1/api/users/login",
        json={"email": "invalid@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid credentials"


def test_get_user_profile(client):
    """Test retrieving the user profile."""
    # Register and log in a user
    client.post(
        "/v1/api/users/register",
        json={"email": "profile@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/v1/api/users/login",
        json={"email": "profile@example.com", "password": "password123"},
    )
    token = login_response.get_json()["token"]

    # Get the profile using the token
    access_token = jwt.decode(
        token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
    )
    assert access_token["id"]
    response = client.get(
        "/v1/api/users/profile",
        headers={"x-access-token": access_token},
    )
    assert response.status_code == 200
    assert response.get_json()["email"] == "profile@example.com"
