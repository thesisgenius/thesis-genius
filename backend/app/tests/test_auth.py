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

def test_logout_user(client):
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

    # Attempt to access a protected route
    response = client.get("/api/thesis/theses", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 401
    assert response.json["success"] is False

def test_deactivate_user(client):
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

    # Attempt to log in again
    response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 401
    assert response.json["success"] is False


def test_activate_user(client):
    """
    Test activating a deactivated user account.
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
    client.put("/api/user/deactivate", headers={
        "Authorization": f"Bearer {token}"
    })

    # Activate the user
    activate_response = client.put("/api/user/activate", headers={
        "Authorization": f"Bearer {token}"
    })
    assert activate_response.status_code == 200
    assert activate_response.json["success"] is True

    # Log in again
    response = client.post("/api/auth/signin", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json


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
