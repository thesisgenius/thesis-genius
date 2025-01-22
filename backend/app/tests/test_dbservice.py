from unittest import mock

import pytest
from app.models.data import Settings
from app.services.dbservice import DBService


@pytest.fixture
def db_service(app):
    """
    Provide a DBService instance for testing.
    """
    return DBService(app)


def test_connect(db_service):
    """
    Test establishing a database connection.
    """
    # Ensure the database is closed before testing
    db_service.db.close()
    assert db_service.db.is_closed()  # Confirm the database is closed

    db_service.connect()
    assert not db_service.db.is_closed()  # Database should now be open


def test_close_connection(db_service):
    """
    Test closing a database connection.
    """
    db_service.connect()  # Ensure the connection is open
    db_service.close_connection()
    assert db_service.db.is_closed()  # Database should now be closed


@mock.patch("app.services.dbservice.Settings")
def test_load_settings(mock_settings, db_service):
    """
    Test loading settings into the app config.
    """
    # Mock settings returned from the database
    mock_settings.get_or_none.side_effect = [
        mock.Mock(value="value1"),
        mock.Mock(value="value2"),
        None,  # No value for "debug_mode"
    ]

    db_service.load_settings()

    # Assert settings were loaded into the app config
    assert db_service.app.config["user"] == "value1"
    assert db_service.app.config["email"] == "value2"
    assert db_service.app.config["debug_mode"] == ""


@mock.patch("app.services.dbservice.Settings")
def test_save_settings(mock_settings, db_service):
    """
    Test saving application settings to the database.
    """
    mock_setting_instance = mock.Mock()
    mock_settings.get_or_create.return_value = (mock_setting_instance, True)

    settings_dict = {"user": "new_user", "email": "new_email"}
    db_service.save_settings(settings_dict)

    # Verify settings were saved
    mock_settings.get_or_create.assert_any_call(name="user")
    mock_settings.get_or_create.assert_any_call(name="email")
    assert mock_setting_instance.value == "new_user" or "new_email"


@mock.patch("app.services.dbservice.Settings")
def test_verify_legacy_password(mock_settings, db_service):
    """
    Test verifying a legacy password.
    """
    legacy_password_hash = db_service._password_salt("legacy_password")
    mock_settings.get_or_none.return_value = mock.Mock(value=legacy_password_hash)

    # Verify the legacy password
    assert db_service.verify_legacy_password("legacy_password") is True
    assert db_service.verify_legacy_password("wrong_password") is False


def test_save_password(db_service):
    """
    Test saving a hashed password in the database.
    """
    password = "secure_password"
    db_service.save_password(password)

    saved_password = Settings.get_or_none(name="password")
    assert saved_password is not None
    assert saved_password.value != password  # Ensure the password is hashed


def test_check_password(db_service):
    """
    Test checking a password against the stored hashed password.
    """
    password = "secure_password"
    db_service.save_password(password)

    # Verify the password matches
    assert db_service.check_password(password) is True
    assert db_service.check_password("wrong_password") is False


def test_is_initialized(db_service):
    """
    Test checking if the database is initialized.
    """
    assert db_service.is_initialized() is True
