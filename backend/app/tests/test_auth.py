import pytest
from app.models.data import Role, User


@pytest.fixture
def create_role():
    """
    Fixture to create default roles in the database.
    """
    for role_name in ["Student", "Teacher", "Admin"]:
        Role.get_or_create(name=role_name)


@pytest.fixture
def register_user(client, create_role):
    """
    Fixture to register a standard user.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "username": "testuser",
            "institution": "National University",
            "password": "password123",
            "role": "Student",
        },
    )
    assert response.status_code == 201
    return response


@pytest.fixture
def login_user(client, register_user):
    """
    Fixture to log in a standard user and return the JWT token.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "token" in response.json
    return response.json["token"]


@pytest.fixture
def register_admin_user(client, create_role):
    """
    Fixture to register an admin user.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "institution": "National University",
            "username": "adminuser",
            "password": "adminpassword123",
            "role": "Admin",
        },
    )
    assert response.status_code == 201

    # Promote the user to admin in the database
    admin_user = User.get_or_none(User.email == "admin@example.com")
    assert admin_user is not None
    assert admin_user.is_admin

    return response


@pytest.fixture
def login_admin_user(client, register_admin_user):
    """
    Fixture to log in an admin user and return the JWT token.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "admin@example.com", "password": "adminpassword123"},
    )
    assert response.status_code == 200
    assert "token" in response.json
    return response.json["token"]


def test_register_user(client, create_role):
    """
    Test user registration.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "institution": "National University",
            "username": "newuser",
            "password": "password456",
            "role": "Student",
        },
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "User registered successfully" in response.json["message"]


def test_register_user_missing_fields(client, create_role):
    """
    Test user registration with missing fields.
    """
    response = client.post(
        "/api/auth/register", json={"first_name": "Incomplete", "last_name": "User"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert (
        "First name, last name, email, institution and password are required"
        in response.json["message"]
    )


def test_register_user_duplicate_email(client, register_user, create_role):
    """
    Test user registration with a duplicate email.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "first_name": "Duplicate",
            "last_name": "User",
            "email": "test@example.com",
            "username": "duplicateuser",
            "password": "password123",
            "role": "Student",
            "institution": "Test University",
        },
    )
    assert response.status_code == 409
    assert response.json["success"] is False
    assert "Email might already be in use" in response.json["message"]


def test_signin_user(client, register_user):
    """
    Test user sign-in.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "token" in response.json


def test_signout_blacklists_token(client, login_user, mock_redis):
    """
    Test that signing out blacklists the user's token.
    """
    token = login_user

    # Ensure the token is not blacklisted initially
    redis_client = mock_redis
    assert redis_client.exists(f"blacklist:{token}") == 0

    # Sign out the user
    response = client.post(
        "/api/auth/signout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True

    # Ensure the token is now blacklisted
    assert redis_client.exists(f"blacklist:{token}") == 1


def test_activate_user(client, login_admin_user, register_user):
    """
    Test activating a user account (admin functionality).
    """
    admin_token = login_admin_user
    from app.models.data import User

    target_user = User.get_or_none(User.email == "test@example.com")
    assert target_user is not None

    # Deactivate the user
    target_user.is_active = False
    target_user.save()
    target_user.refresh_from_db()
    assert not target_user.is_active  # Ensure the user is inactive

    # Activate the user as admin
    response = client.put(
        f"/api/user/activate/{target_user.id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "User activated successfully" in response.json["message"]

    # Verify the user's account is now active
    target_user.refresh_from_db()
    assert target_user.is_active is True
