from backend.app.models.data import Settings


def test_connect(db_service):
    """
    Test establishing a database connection.
    """
    db_service.db.close()  # Ensure the database is closed before testing
    db_service.connect()
    assert not db_service.db.is_closed()  # Database should now be open


def test_close_connection(db_service):
    """
    Test closing a database connection.
    """
    db_service.connect()
    db_service.close_connection()
    assert db_service.db.is_closed()  # Database should now be closed


def test_is_initialized(db_service):
    """
    Test checking if the database is initialized.
    """
    assert db_service.is_initialized() is True  # Database should be initialized


def test_load_settings(db_service):
    """
    Test loading settings into the app config.
    """
    # Add settings to the database
    Settings.create(name="user", value="value1")
    Settings.create(name="email", value="value2")

    # Load settings
    db_service.load_settings()

    assert db_service.app.config["user"] == "value1"
    assert db_service.app.config["email"] == "value2"
    assert db_service.app.config["debug_mode"] == ""  # Default to empty string


def test_save_settings(db_service):
    """
    Test saving application settings to the database.
    """
    settings_dict = {"user": "new_user", "email": "new_email"}
    db_service.save_settings(settings_dict)

    # Verify settings are saved
    saved_user = Settings.get_or_none(name="user")
    saved_email = Settings.get_or_none(name="email")

    assert saved_user.value == "new_user"
    assert saved_email.value == "new_email"


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


def test_verify_legacy_password(db_service):
    """
    Test verifying a legacy password.
    """
    legacy_password_hash = db_service._password_salt("legacy_password")
    Settings.create(name="password", value=legacy_password_hash)

    # Verify the legacy password
    assert db_service.verify_legacy_password("legacy_password") is True
    assert db_service.verify_legacy_password("wrong_password") is False
