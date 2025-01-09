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
    assert token is not None

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
    assert token is not None

    # Fetch posts
    response = client.get(
        "/api/forum/posts", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json["posts"], list)

def test_add_comment_to_post(client):
    """
    Test adding a comment to a forum post.
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

    # Create a post
    post_response = client.post("/api/forum/posts", json={
        "title": "Test Post",
        "content": "This is a test post."
    }, headers={"Authorization": f"Bearer {token}"})
    post_id = post_response.json["id"]
    assert post_id is not None

    # Add a comment to the post
    comment_response = client.post(f"/api/forum/posts/{post_id}/comments", json={
        "content": "This is a test comment."
    }, headers={"Authorization": f"Bearer {token}"})
    assert comment_response.status_code == 201
    assert comment_response.json["success"] is True
