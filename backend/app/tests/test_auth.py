import pytest

@pytest.fixture
def register_user(client):
    """
    Fixture to register a user.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    return response


@pytest.fixture
def login_user(client, register_user):
    """
    Fixture to log in a user and return the JWT token.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "token" in response.json
    return response.json["token"]

@pytest.fixture
def register_admin_user(client):
    """
    Fixture to register an admin user.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "adminpassword123",
        },
    )
    assert response.status_code == 201

    # Promote the user to admin in the database
    from backend.app.models.data import User
    admin_user = User.get_or_none(User.email == "admin@example.com")
    assert admin_user is not None
    admin_user.is_admin = True
    admin_user.save()

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

def test_register_user(client):
    """
    Test user registration.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password456",
        },
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "User registered successfully" in response.json["message"]


def test_register_user_missing_fields(client):
    """
    Test user registration with missing fields.
    """
    response = client.post(
        "/api/auth/register", json={"name": "Incomplete User"}
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Name, email, and password are required" in response.json["message"]


def test_register_user_duplicate_email(client, register_user):
    """
    Test user registration with a duplicate email.
    """
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Duplicate User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
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


def test_signin_user_invalid_credentials(client):
    """
    Test user sign-in with invalid credentials.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Invalid credentials" in response.json["message"]


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


def test_blacklisted_token_rejected(client, login_user, mock_redis):
    """
    Test that a blacklisted token is rejected when accessing protected routes.
    """
    token = login_user

    # Blacklist the token
    redis_client = mock_redis
    redis_client.setex(f"blacklist:{token}", 3600, "true")

    # Attempt to access a protected route with the blacklisted token
    response = client.get(
        "/api/user/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Token is expired and blacklisted" in response.json["message"]


def test_deactivate_user(client, login_user, mock_redis):
    """
    Test deactivating a user account.
    """
    token = login_user
    from backend.app.models.data import User
    target_user = User.get_or_none(User.email == "test@example.com")
    assert target_user is not None
    assert target_user.is_active  # Ensure the user is inactive

    # Deactivate the user
    response = client.put(
        "/api/user/deactivate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True

    # Ensure the user's token is blacklisted
    redis_client = mock_redis
    assert redis_client.exists(f"blacklist:{token}") == 1

    # Verify the user's account is now inactive
    target_user.refresh_from_db()
    assert not target_user.is_active  # Ensure the user is inactive

def test_activate_user(client, login_user, login_admin_user, register_user):
    """
    Test activating a user account (admin functionality).
    """
    admin_token = login_admin_user

    # Create a regular user (already registered via the register_user fixture)
    token = login_user
    from backend.app.models.data import User
    target_user = User.get_or_none(User.email == "test@example.com")
    assert target_user is not None

    # Deactivate the user
    response = client.put(
        "/api/user/deactivate",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
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