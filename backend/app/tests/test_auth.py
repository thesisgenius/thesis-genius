import pytest

def test_register_user(client):
    """
    Test user registration.
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
    assert response.json["success"] is True

def test_login_user(client):
    """
    Test user login.
    """
    # Register a user first
    client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )

    # Log in with the registered user
    response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "token" in response.json

def test_logout_user(client, mock_redis):
    """
    Test logging out a user.
    """
    # Register and log in a user
    client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = login_response.json["token"]
    assert token is not None

    # Log out the user
    logout_response = client.post("/api/auth/signout", headers={
        "Authorization": f"Bearer {token}"
    })
    assert logout_response.status_code == 200
    assert logout_response.json["success"] is True

    # Check Redis for token invalidation
    redis_client = mock_redis
    blacklisted = redis_client.exists(f"blacklist:{token}")
    print(f"Redis blacklisted: {blacklisted}")
    assert blacklisted == 1

    # Attempt to access a protected route
    response = client.get("/api/thesis/theses", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json["success"] is False

def test_deactivate_user(client, mock_redis):
    """
    Test deactivating a user account.
    """
    # Register and log in a user
    client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    token = login_response.json["token"]
    assert token is not None

    # Deactivate the user
    deactivate_response = client.put("/api/user/deactivate", headers={
        "Authorization": f"Bearer {token}"
    })
    assert deactivate_response.status_code == 200
    assert deactivate_response.json["success"] is True

    # Check Redis for token invalidation
    redis_client = mock_redis
    blacklisted = redis_client.exists(f"blacklist:{token}")
    print(f"Redis blacklisted: {blacklisted}")
    assert blacklisted == 1

    # Attempt to log in again
    response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json["success"] is False

def register_admin_user(client):
    """
    Register and log in an admin user.
    """
    # Create an admin user
    from backend.app.models.data import User
    client.post("/api/auth/register", json={
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpassword"
    })

    # Update the user to set `is_admin = True`
    admin_user = User.get_or_none(User.email == "admin@example.com")
    admin_user.is_admin = True
    admin_user.save()

    # Log in as the admin
    login_response = client.post("/api/auth/signin", json={
        "email": "admin@example.com",
        "password": "adminpassword"
    })
    return login_response.json["token"]

def test_activate_user(client):
    """
    Test activating a deactivated user account with an admin user.
    """
    # Register and log in a regular user
    client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    login_response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    user_token = login_response.json["token"]
    assert user_token is not None

    # Deactivate the regular user
    deactivate_response = client.put("/api/user/deactivate", headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert deactivate_response.status_code == 200
    assert deactivate_response.json["success"] is True

    # Register and log in as admin
    admin_token = register_admin_user(client)
    assert admin_token is not None

    # Activate the regular user with the admin's privileges
    from backend.app.models.data import User
    user_id = User.get_or_none(User.email == "test@example.com").get_id()
    activate_response = client.put(f"/api/user/activate/{user_id}", headers={
        "Authorization": f"Bearer {admin_token}"
    })
    assert activate_response.status_code == 200
    assert activate_response.json["success"] is True

    # Verify that the regular user is active
    activated_user = User.get_or_none(User.id == user_id)
    assert activated_user.is_active is True

def test_login_invalid_credentials(client):
    """
    Test login with invalid credentials.
    """
    response = client.post(
        "/api/auth/signin",
        json={"email": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json["success"] is False

def test_register_missing_fields(client):
    """
    Test registration with missing required fields.
    """
    response = client.post("/api/auth/register", json={
        "email": "test@example.com"  # Missing 'name' and 'password'
    })
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "message" in response.json

def test_access_with_invalid_token(client):
    """
    Test access to a protected route with an invalid token.
    """
    response = client.get("/api/thesis/theses", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "message" in response.json

def test_register_duplicate_email(client):
    """
    Test registering a user with an already registered email.
    """
    client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "password123"
    })

    response = client.post("/api/auth/register", json={
        "name": "Another User",
        "email": "duplicate@example.com",
        "password": "password456"
    })

    assert response.status_code == 400
    assert response.json["success"] is False
    assert "message" in response.json
