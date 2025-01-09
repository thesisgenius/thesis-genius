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
