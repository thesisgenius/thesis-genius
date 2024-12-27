import os
import sys

import pytest
from dotenv import load_dotenv

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


def test_create_thesis(client):
    response = client.post(
        "/v1/api/thesis/",
        json={
            "title": "Test Thesis",
            "author": "John Doe",
            "abstract": "An example thesis for testing.",
            "status": "In Progress",
            "submission_date": "2024-12-25",
        },
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["message"] == "Thesis created successfully."


def test_get_all_theses(client):
    # Create a sample thesis first
    client.post(
        "/v1/api/thesis/",
        json={
            "title": "Test Thesis",
            "author": "John Doe",
            "abstract": "An example thesis for testing.",
            "status": "In Progress",
            "submission_date": "2024-12-25",
        },
    )

    response = client.get("/v1/api/thesis/all")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Thesis"


def test_get_single_thesis(client):
    # Create a sample thesis first
    post_response = client.post(
        "/v1/api/thesis/",
        json={
            "title": "Test Thesis",
            "author": "John Doe",
            "abstract": "An example thesis for testing.",
            "status": "In Progress",
            "submission_date": "2024-12-25",
        },
    )

    assert (
        post_response.status_code == 201
    ), f"Unexpected status code: {post_response.status_code}, Response: {post_response.data.decode()}"
    post_data = post_response.get_json()
    assert (
        post_data is not None
    ), f"Response JSON is None, Response: {post_response.data.decode()}"
    thesis_id = post_response.get_json()["id"]
    print(post_response.data.decode())

    response = client.get(f"/v1/api/thesis/{thesis_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Test Thesis"
    assert data["author"] == "John Doe"


def test_update_thesis(client):
    # Create a sample thesis first
    post_response = client.post(
        "/v1/api/thesis/",
        json={
            "title": "Test Thesis",
            "author": "John Doe",
            "abstract": "An example thesis for testing.",
            "status": "In Progress",
            "submission_date": "2024-12-25",
        },
    )
    thesis_id = post_response.get_json()["id"]

    # Update the thesis
    response = client.put(
        f"/v1/api/thesis/{thesis_id}",
        json={"title": "Updated Thesis", "status": "Completed"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Thesis updated successfully."

    # Verify the update
    get_response = client.get(f"/v1/api/thesis/{thesis_id}")
    updated_data = get_response.get_json()
    assert updated_data["title"] == "Updated Thesis"
    assert updated_data["status"] == "Completed"


def test_delete_thesis(client):
    # Create a sample thesis first
    post_response = client.post(
        "/v1/api/thesis/",
        json={
            "title": "Test Thesis",
            "author": "John Doe",
            "abstract": "An example thesis for testing.",
            "status": "In Progress",
            "submission_date": "2024-12-25",
        },
    )
    thesis_id = post_response.get_json()["id"]

    # Delete the thesis
    response = client.delete(f"/v1/api/thesis/{thesis_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Thesis deleted successfully."

    # Verify the deletion
    get_response = client.get(f"/v1/api/thesis/{thesis_id}")
    assert get_response.status_code == 404
