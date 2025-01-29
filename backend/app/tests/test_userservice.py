from unittest.mock import MagicMock, patch

import pytest
from app.services.userservice import UserService


@pytest.fixture
def user_service():
    """Fixture for initializing UserService with a mock logger."""
    logger = MagicMock()
    return UserService(logger)


def test_change_user_status_success_activate(user_service):
    """Test successfully activating a user."""
    mock_user = MagicMock()
    user_service._get_user_by_id = MagicMock(return_value=mock_user)

    result = user_service.change_user_status(user_id=1, is_active=True)

    assert result is True
    assert mock_user.is_active is True
    mock_user.save.assert_called_once()
    user_service.logger.info.assert_called_with("User 1 activated successfully.")


def test_change_user_status_success_deactivate(user_service):
    """Test successfully deactivating a user."""
    mock_user = MagicMock()
    user_service._get_user_by_id = MagicMock(return_value=mock_user)

    result = user_service.change_user_status(user_id=1, is_active=False)

    assert result is True
    assert mock_user.is_active is False
    mock_user.save.assert_called_once()
    user_service.logger.info.assert_called_with("User 1 deactivated successfully.")


def test_change_user_status_user_not_found(user_service):
    """Test changing status when user is not found."""
    # Mock `_get_user_by_id` to simulate a missing user
    user_service._get_user_by_id = MagicMock(return_value=None)

    with patch("flask.abort") as mock_abort:
        user_service.change_user_status(user_id=1, is_active=True)
        # Verify `abort(404)` is called exactly once
        mock_abort.assert_called_once_with(404, description="User not found.")


def test_change_user_status_with_token(user_service):
    """Test changing user status with token invalidation."""
    mock_user = MagicMock()
    user_service._get_user_by_id = MagicMock(return_value=mock_user)

    with patch("app.services.userservice.blacklist_token") as mock_blacklist_token:
        result = user_service.change_user_status(
            user_id=1, is_active=False, token="test_token"
        )

        assert result is True
        assert mock_user.is_active is False
        mock_user.save.assert_called_once()
        mock_blacklist_token.assert_called_once_with("test_token")
        user_service.logger.info.assert_any_call("JWT token invalidated for user 1.")
        user_service.logger.info.assert_any_call("User 1 deactivated successfully.")


def test_change_user_status_internal_error(user_service):
    """Test handling an internal server error when changing user status."""
    user_service._get_user_by_id = MagicMock(side_effect=Exception("Unexpected error"))

    with patch("flask.abort") as mock_abort:
        user_service.change_user_status(user_id=1, is_active=True)
        mock_abort.assert_called_once_with(500, description="Internal server error.")
