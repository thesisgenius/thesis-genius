import os
import sys

import pytest

from server import db
from server.app import create_app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def client():
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def create_test_user(client, email, password):
    """Test registering a new user."""
    response = client.post(
        "/v1/api/users/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def test_create_forum(client):
    user_id = create_test_user(client, "test_user1@example.com", "password123")
    response = client.post(
        "/v1/api/forum/posts",
        json={
            "user_id": user_id,
            "title": "Test Forum",
            "description": "A test forum",
            "body": "This is the body of the test forum.",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["message"] == "Forum created"


def test_get_forum(client):
    user_id = create_test_user(client, "test_user1@example.com", "password123")
    client.post(
        "/v1/api/forum/posts",
        json={
            "user_id": user_id,
            "title": "Test Forum",
            "description": "A test forum",
            "body": "This is the body of the test forum.",
        },
    )
    response = client.get("/v1/api/forum/posts/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Forum"
    assert data["body"] == "This is the body of the test forum."


def test_update_forum(client):
    user_id = create_test_user(client, "test_user1@example.com", "password123")
    client.post(
        "/v1/api/forum/posts",
        json={
            "user_id": user_id,
            "title": "Test Forum",
            "description": "A test forum",
            "body": "This is the body of the test forum.",
        },
    )
    response = client.put(
        "/v1/api/forum/posts/1",
        json={
            "title": "Updated Title",
            "description": "Updated description",
            "body": "Updated body content.",
        },
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Forum updated"
    updated_response = client.get("/v1/api/forum/posts/1")
    data = updated_response.get_json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated description"


def test_delete_forum(client):
    user_id = create_test_user(client, "test_user1@example.com", "password123")
    client.post(
        "/v1/api/forum/posts",
        json={
            "user_id": user_id,
            "title": "Test Forum",
            "description": "A test forum",
            "body": "This is the body of the test forum.",
        },
    )
    response = client.delete("/v1/api/forum/posts/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Forum deleted"
    response = client.get("/v1/api/forum/posts/1")
    assert response.status_code == 404
