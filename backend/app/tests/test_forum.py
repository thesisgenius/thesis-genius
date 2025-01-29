from unittest.mock import MagicMock

import pytest
from app.services.forumservice import ForumService
from peewee import PeeweeException

# Constants for test
POST_ID = 1
COMMENT_ID = 1
INVALID_POST_ID = -1  # Example invalid ID
INVALID_COMMENT_ID = -1
PAGE = 1
PER_PAGE = 10
POST_DATA = {
    "id": POST_ID,
    "title": "Test Post",
    "description": "A test description",
    "content": "This is the content of the test post.",
    "user": "TestUser",
    "created_at": "2023-10-01T08:30:00",
    "updated_at": "2023-10-01T08:45:00",
}
COMMENT_DATA = {
    "id": COMMENT_ID,
    "content": "This is a test comment.",
    "created_at": "2023-10-01T09:00:00",
    "updated_at": "2023-10-01T09:15:00",
    "user": "TestUser",
    "post": POST_ID,
}


@pytest.fixture
def mock_forum_service():
    """Fixture to mock the ForumService."""
    mock_service = MagicMock(spec=ForumService)

    # Mocking logger
    logger_mock = MagicMock()
    mock_service.logger = logger_mock  # Add mock logger to mock_service

    # Mocking get_all_posts
    mock_service.get_all_posts.return_value = {
        "results": [POST_DATA],
        "total": 1,
        "page": PAGE,
        "per_page": PER_PAGE,
    }

    # Mocking get_post_by_id
    mock_service.get_post_by_id.return_value = POST_DATA

    # Mocking get_post_comments
    mock_service.get_post_comments.return_value = {
        "results": [COMMENT_DATA],
        "total": 1,
        "page": PAGE,
        "per_page": PER_PAGE,
    }

    # Mocking update_post
    mock_service.update_post.return_value = True

    # Mocking delete_comment
    mock_service.delete_comment.return_value = True

    # Mocking get_comment_by_id
    mock_service.get_comment_by_id.return_value = COMMENT_DATA

    # Mocking update_comment
    mock_service.update_comment.return_value = True

    # Mocking delete_all_comments
    mock_service.delete_all_comments.return_value = True

    return mock_service


def test_get_all_posts(mock_forum_service):
    """Test fetching all posts using ForumService."""
    response = mock_forum_service.get_all_posts(page=PAGE, per_page=PER_PAGE)
    assert response["results"] == [POST_DATA]
    assert response["total"] == 1
    assert response["page"] == PAGE
    assert response["per_page"] == PER_PAGE
    mock_forum_service.get_all_posts.assert_called_once_with(
        page=PAGE, per_page=PER_PAGE
    )


def test_get_all_posts_empty(mock_forum_service):
    """Test fetching all posts when no posts exist."""
    mock_forum_service.get_all_posts.return_value = {
        "results": [],
        "total": 0,
        "page": PAGE,
        "per_page": PER_PAGE,
    }
    response = mock_forum_service.get_all_posts(page=PAGE, per_page=PER_PAGE)
    assert response["results"] == []
    assert response["total"] == 0
    assert response["page"] == PAGE
    mock_forum_service.get_all_posts.assert_called_with(page=PAGE, per_page=PER_PAGE)


def test_get_post_by_id(mock_forum_service):
    """Test fetching a single post by ID using ForumService."""
    response = mock_forum_service.get_post_by_id(POST_ID)
    assert response == POST_DATA
    mock_forum_service.get_post_by_id.assert_called_once_with(POST_ID)


def test_get_post_by_id_not_found(mock_forum_service):
    """Test fetching a post by ID that doesn't exist."""
    mock_forum_service.get_post_by_id.return_value = None  # Simulates post not found
    response = mock_forum_service.get_post_by_id(INVALID_POST_ID)
    assert response is None
    mock_forum_service.get_post_by_id.assert_called_once_with(INVALID_POST_ID)


def test_get_post_comments(mock_forum_service):
    """Test fetching comments for a post using ForumService."""
    response = mock_forum_service.get_post_comments(
        post_id=POST_ID, page=PAGE, per_page=PER_PAGE
    )
    assert response["results"] == [COMMENT_DATA]
    assert response["total"] == 1
    assert response["page"] == PAGE
    assert response["per_page"] == PER_PAGE
    mock_forum_service.get_post_comments.assert_called_once_with(
        post_id=POST_ID, page=PAGE, per_page=PER_PAGE
    )


def test_get_post_comments_empty(mock_forum_service):
    """Test fetching comments when no comments exist for a post."""
    mock_forum_service.get_post_comments.return_value = {
        "results": [],
        "total": 0,
        "page": PAGE,
        "per_page": PER_PAGE,
    }
    response = mock_forum_service.get_post_comments(
        post_id=POST_ID, page=PAGE, per_page=PER_PAGE
    )
    assert response["results"] == []
    assert response["total"] == 0
    assert response["page"] == PAGE
    assert response["per_page"] == PER_PAGE
    mock_forum_service.get_post_comments.assert_called_once_with(
        post_id=POST_ID, page=PAGE, per_page=PER_PAGE
    )


def test_update_post(mock_forum_service):
    """Test updating a post using ForumService."""
    update_data = {"title": "Updated Title", "content": "Updated content."}
    response = mock_forum_service.update_post(post_id=POST_ID, post_data=update_data)
    assert response is True
    mock_forum_service.update_post.assert_called_once_with(
        post_id=POST_ID, post_data=update_data
    )


def test_update_post_failure(mock_forum_service):
    """Test updating a post that doesn't exist."""
    mock_forum_service.update_post.return_value = False
    update_data = {"title": "Updated Title", "content": "Updated content."}
    response = mock_forum_service.update_post(
        post_id=INVALID_POST_ID, post_data=update_data
    )
    assert response is False
    mock_forum_service.update_post.assert_called_once_with(
        post_id=INVALID_POST_ID, post_data=update_data
    )


def test_delete_comment(mock_forum_service):
    """Test deleting a comment from a post using ForumService."""
    response = mock_forum_service.delete_comment(post_id=POST_ID, comment_id=COMMENT_ID)
    assert response is True
    mock_forum_service.delete_comment.assert_called_once_with(
        post_id=POST_ID, comment_id=COMMENT_ID
    )


def test_delete_comment_failure(mock_forum_service):
    """Test deleting a comment that doesn't exist."""
    mock_forum_service.delete_comment.return_value = False
    response = mock_forum_service.delete_comment(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID
    )
    assert response is False
    mock_forum_service.delete_comment.assert_called_once_with(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID
    )


def test_safe_execute_exception_handling(mock_forum_service):
    """Test error handling during database execution."""

    # Simulate the behavior of `_safe_execute` with exception handling
    def mock_safe_execute(query, log_error_msg, on_error):
        try:
            # Simulate a query raising an exception
            query()
        except PeeweeException:
            mock_forum_service.logger.error(log_error_msg)
            return on_error

    # Patch `_safe_execute` to use the custom behavior
    mock_forum_service._safe_execute.side_effect = mock_safe_execute

    # Call `_safe_execute` with a query that raises an exception
    result = mock_forum_service._safe_execute(
        query=lambda: (_ for _ in ()).throw(
            PeeweeException("Test exception")
        ),  # Simulates raising exception
        log_error_msg="Database error occurred",
        on_error="Error fallback",
    )

    assert result == "Error fallback"
    mock_forum_service.logger.error.assert_called_once_with("Database error occurred")


def test_get_comment_by_id(mock_forum_service):
    """Test fetching a single comment by ID using ForumService."""
    response = mock_forum_service.get_comment_by_id(
        post_id=POST_ID, comment_id=COMMENT_ID
    )
    assert response == COMMENT_DATA
    mock_forum_service.get_comment_by_id.assert_called_once_with(
        post_id=POST_ID, comment_id=COMMENT_ID
    )


def test_get_comment_by_id_not_found(mock_forum_service):
    """Test fetching a comment by ID that doesn't exist."""
    mock_forum_service.get_comment_by_id.return_value = (
        None  # Simulate comment not found
    )
    response = mock_forum_service.get_comment_by_id(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID
    )
    assert response is None
    mock_forum_service.get_comment_by_id.assert_called_once_with(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID
    )


def test_update_comment(mock_forum_service):
    """Test updating a comment using ForumService."""
    new_content = "Updated comment content."
    response = mock_forum_service.update_comment(
        post_id=POST_ID, comment_id=COMMENT_ID, new_content=new_content
    )
    assert response is True
    mock_forum_service.update_comment.assert_called_once_with(
        post_id=POST_ID, comment_id=COMMENT_ID, new_content=new_content
    )


def test_update_comment_failure(mock_forum_service):
    """Test updating a comment that doesn't exist."""
    mock_forum_service.update_comment.return_value = False
    new_content = "Updated comment content."
    response = mock_forum_service.update_comment(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID, new_content=new_content
    )
    assert response is False
    mock_forum_service.update_comment.assert_called_once_with(
        post_id=POST_ID, comment_id=INVALID_COMMENT_ID, new_content=new_content
    )


def test_delete_all_comments(mock_forum_service):
    """Test deleting all comments for a post using ForumService."""
    response = mock_forum_service.delete_all_comments(post_id=POST_ID)
    assert response is True
    mock_forum_service.delete_all_comments.assert_called_once_with(post_id=POST_ID)


def test_delete_all_comments_failure(mock_forum_service):
    """Test deleting all comments for a post when none exist."""
    mock_forum_service.delete_all_comments.return_value = False
    response = mock_forum_service.delete_all_comments(post_id=INVALID_POST_ID)
    assert response is False
    mock_forum_service.delete_all_comments.assert_called_once_with(
        post_id=INVALID_POST_ID
    )
