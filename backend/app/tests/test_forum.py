def test_create_post(client):
    """
    Test creating a forum post.
    """
    # Register and log in a user
    client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json["token"]

    # Create a post
    response = client.post(
        "/api/forum/posts",
        json={"title": "Test Post", "content": "This is a test post."},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True


def test_get_posts(client):
    """
    Test fetching forum posts.
    """
    # Register and log in a user
    client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/api/auth/signin",
        json={"email": "test@example.com", "password": "password123"},
    )
    token = login_response.json["token"]

    # Fetch posts
    response = client.get(
        "/api/forum/posts", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json["posts"], list)
