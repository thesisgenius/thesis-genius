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
def user_token(client, create_role):
    """
    Fixture to register and log in a user, returning a valid JWT token.
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
def create_post(client, user_token):
    """
    Fixture to create a post and return the post data.
    """
    response = client.post(
        "/api/forum/posts",
        json={"title": "Fixture Post", "content": "This is a fixture post."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    return response.json


@pytest.fixture
def create_comment(client, user_token, create_post):
    """
    Fixture to create a comment on a post and return the comment data.
    """
    post_id = create_post["id"]
    response = client.post(
        f"/api/forum/posts/{post_id}/comments",
        json={"content": "This is a fixture comment."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    return response.json


def test_create_post(client, user_token):
    """
    Test creating a forum post.
    """
    response = client.post(
        "/api/forum/posts",
        json={"title": "Test Post", "content": "This is a test post."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "id" in response.json
    assert response.json["post"] == "Test Post"


def test_create_post_missing_fields(client, user_token):
    """
    Test creating a post with missing fields.
    """
    response = client.post(
        "/api/forum/posts",
        json={"title": "Incomplete Post"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Title and content are required" in response.json["message"]


def test_list_posts(client, create_post):
    """
    Test fetching forum posts with pagination.
    """
    response = client.get("/api/forum/posts?page=1&per_page=10")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert isinstance(response.json["posts"], list)
    assert len(response.json["posts"]) > 0
    assert "page" in response.json
    assert "per_page" in response.json
    assert "total" in response.json


def test_view_post(client, create_post, create_comment):
    """
    Test fetching a single post with its comments.
    """
    post_id = create_post["id"]
    response = client.get(f"/api/forum/posts/{post_id}?page=1&per_page=10")
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "post" in response.json
    assert "comments" in response.json
    assert len(response.json["comments"]["comments"]) > 0


def test_add_comment_to_post(client, create_post, user_token):
    """
    Test adding a comment to a forum post.
    """
    post_id = create_post["id"]
    response = client.post(
        f"/api/forum/posts/{post_id}/comments",
        json={"content": "This is a test comment."},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert response.json["comment"] == "This is a test comment."


def test_add_comment_missing_content(client, create_post, user_token):
    """
    Test adding a comment to a post with missing content.
    """
    post_id = create_post["id"]
    response = client.post(
        f"/api/forum/posts/{post_id}/comments",
        json={},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Content is required" in response.json["message"]


def test_add_comment_unauthorized(client, create_post):
    """
    Test adding a comment to a post without authentication.
    """
    post_id = create_post["id"]
    response = client.post(
        f"/api/forum/posts/{post_id}/comments",
        json={"content": "This is a test comment."},
    )
    assert response.status_code == 401
    assert response.json["success"] is False


def test_delete_post(client, create_post, user_token):
    """
    Test deleting a forum post.
    """
    post_id = create_post["id"]
    response = client.delete(
        f"/api/forum/posts/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "Post deleted successfully" in response.json["message"]
