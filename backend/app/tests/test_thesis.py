def test_create_thesis(client):
    """
    Test creating a thesis.
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

    # Create a thesis
    response = client.post("/api/thesis/thesis", json={
        "title": "Test Thesis",
        "abstract": "This is a test thesis.",
        "status": "Pending",
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    assert response.json["success"] is True


def test_get_theses(client):
    """
    Test fetching theses for a user.
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

    # Fetch theses
    response = client.get("/api/thesis/theses", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json["theses"], list)
