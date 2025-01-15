import pytest

from backend.app.models.data import Role


@pytest.fixture
def create_role():
    """
    Fixture to create default roles in the database.
    """
    for role_name in ["Student", "Teacher", "Admin"]:
        Role.get_or_create(name=role_name)


@pytest.fixture
def register_and_login_user(client, create_role):
    """
    Fixture to register and log in a user, returning the JWT token.
    """
    client.post(
        "/api/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
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


@pytest.fixture
def create_thesis(client, register_and_login_user):
    """
    Fixture to create a thesis, returning the thesis data.
    """
    token = register_and_login_user
    response = client.post(
        "/api/thesis/thesis",
        json={
            "title": "Test Thesis",
            "abstract": "This is a test thesis.",
            "status": "Pending",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    return response.json


def test_create_thesis(client, register_and_login_user):
    """
    Test creating a thesis.
    """
    token = register_and_login_user
    response = client.post(
        "/api/thesis/thesis",
        json={
            "title": "Test Thesis",
            "abstract": "This is a test thesis.",
            "status": "Pending",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["id"] is not None


def test_create_thesis_missing_fields(client, register_and_login_user):
    """
    Test creating a thesis with missing required fields.
    """
    token = register_and_login_user
    response = client.post(
        "/api/thesis/thesis",
        json={"title": "Incomplete Thesis"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Title, abstract, and status are required" in response.json["message"]


def test_get_theses(client, register_and_login_user, create_thesis):
    """
    Test fetching theses for a user.
    """
    token = register_and_login_user
    response = client.get(
        "/api/thesis/theses", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert isinstance(response.json["theses"], list)
    assert len(response.json["theses"]) > 0


def test_update_thesis(client, create_thesis, register_and_login_user):
    """
    Test updating a thesis.
    """
    token = register_and_login_user
    thesis_id = create_thesis["id"]

    response = client.put(
        f"/api/thesis/thesis/{thesis_id}",
        json={
            "title": "Updated Title",
            "abstract": "Updated Abstract",
            "status": "Approved",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Thesis updated successfully" in response.json["message"]


def test_update_thesis_invalid_id(client, register_and_login_user):
    """
    Test updating a thesis with an invalid ID.
    """
    token = register_and_login_user

    response = client.put(
        "/api/thesis/thesis/99999",
        json={
            "title": "Updated Title",
            "abstract": "Updated Abstract",
            "status": "Approved",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Failed to update thesis" in response.json["message"]


def test_delete_thesis(client, create_thesis, register_and_login_user):
    """
    Test deleting a thesis.
    """
    token = register_and_login_user
    thesis_id = create_thesis["id"]

    response = client.delete(
        f"/api/thesis/thesis/{thesis_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Thesis deleted successfully" in response.json["message"]


def test_delete_thesis_invalid_id(client, register_and_login_user):
    """
    Test deleting a thesis with an invalid ID.
    """
    token = register_and_login_user

    response = client.delete(
        "/api/thesis/thesis/99999",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Failed to delete thesis" in response.json["message"]
