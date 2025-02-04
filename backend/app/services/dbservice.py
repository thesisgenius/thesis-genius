import hashlib

from app.models.data import Settings
from app.utils.db import database_proxy
from werkzeug.security import check_password_hash, generate_password_hash


class DBService:
    """
    Handles database operations, application settings management, and user authentication.

    This class provides methods to establish and close the database connection, manage
    application settings, and handle password saving and verification for authentication.
    It is designed to integrate with a Flask application and uses a database proxy for
    managing the database connection.

    :ivar db: Database proxy instance used to connect to the database.
    :type db: Proxy
    :ivar app: Flask application instance integrating with this service.
    :type app: Flask
    :ivar setting_keys: List of application setting keys to be managed.
    :type setting_keys: list[str]
    """

    def __init__(self, app, setting_keys=None):
        self.db = database_proxy
        self.app = app
        self.setting_keys = setting_keys or ["user", "email", "debug_mode"]

    def connect(self):
        """
        Establishes a connection to the database if it is not already connected.

        Attempts to connect to the database using the provided database instance. Logs
        a message indicating a successful connection or logs an error and raises an
        exception in case of failure.

        :raises Exception: If the database connection fails for any reason.
        :return: None
        """
        try:
            if self.db.is_closed():
                self.db.connect()
                self.app.logger.info("Database connection established.")
        except Exception as e:
            self.app.logger.error(f"Failed to connect to the database: {e}")
            raise

    def close_connection(self):
        """
        Closes the database connection if it is active.

        This method checks if the database connection is currently open. If so, it
        closes the connection and logs the operation. In case of any exceptions, the
        error is logged.

        :raises Exception: If an issue occurs during the closing of the database
            connection.
        """
        try:
            if not self.db.is_closed():
                self.db.close()
                self.app.logger.info("Database connection closed.")
        except Exception as e:
            self.app.logger.error(f"Failed to close the database connection: {e}")

    def is_initialized(self):
        """
        Checks if the database is initialized by verifying if the required table exists.

        This method tries to ascertain whether the database setup has been
        completed by checking for the presence of a specific table. If an
        exception occurs during this process, it logs the associated error
        message and returns a default value indicating the database is not
        initialized.

        :return: A boolean value indicating whether the database is initialized.
                 Returns `True` if the table exists, otherwise `False`.
        :rtype: bool
        """
        try:
            return Settings.table_exists()
        except Exception as e:
            self.app.logger.error(f"Failed to check if database is initialized: {e}")
            return False

    def load_settings(self):
        """
        Loads application settings from a storage and updates the application's
        configuration accordingly. For every key listed in `self.setting_keys`, it
        retrieves the corresponding setting value from the `Settings` storage. If a
        setting is found, its value is set in the application's configuration;
        otherwise, an empty string is set.

        This method logs the success of the operation or reports any errors encountered
        during the process.

        :raises Exception: Logs an error if retrieving or updating the settings fails.
        """
        try:
            for name in self.setting_keys:
                setting = Settings.get_or_none(name=name)
                self.app.config[name] = setting.value if setting else ""
            self.app.logger.info("Application settings loaded successfully.")
        except Exception as e:
            self.app.logger.error(f"Failed to load settings: {e}")

    def save_settings(self, settings_dict):
        """
        Save application settings to the database and refresh the application configuration.

        This method processes a given dictionary of settings, updating or creating
        entries in the database corresponding to the settings. After saving, it reloads
        the updated settings into the application configuration. Any errors during
        this process, such as database failures, are logged.

        :param settings_dict:
            A dictionary where each key represents the name of a setting and each
            value represents the corresponding value to be saved.

        :return:
            None
        """
        try:
            for name, value in settings_dict.items():
                setting, created = Settings.get_or_create(name=name)
                setting.value = value
                setting.save()
            self.load_settings()  # Refresh settings in the app config
            self.app.logger.info("Application settings saved successfully.")
        except Exception as e:
            self.app.logger.error(f"Failed to save settings: {e}")

    def save_password(self, password):
        """
        Save the user's password securely by hashing it and saving it to the database.
        Logs the appropriate message upon success or failure.

        :param password: The plaintext password to be saved.
        :type password: str
        :return: None
        """
        try:
            setting, _ = Settings.get_or_create(name="password")
            setting.value = generate_password_hash(password)
            setting.save()
            self.app.logger.info("Password saved successfully.")
        except Exception as e:
            self.app.logger.error(f"Failed to save password: {e}")

    def check_password(self, password):
        """
        Checks if the provided password matches the stored hashed password.

        This method retrieves the hashed password from the database settings table
        using the key 'password'. It then compares the provided plain-text password
        against the retrieved hashed value. If the password setting does not exist
        or any error occurs during the process, appropriate logs are generated and
        the method will return `False`.

        :param password: The plain-text password input to validate.
        :type password: str
        :return: True if the password matches the hashed value, False otherwise.
        :rtype: bool
        """
        try:
            setting = Settings.get_or_none(name="password")
            if setting and setting.value:
                return check_password_hash(setting.value, password)
            self.app.logger.warning("Password not found.")
            return False
        except Exception as e:
            self.app.logger.error(f"Failed to check password: {e}")
            return False

    def verify_legacy_password(self, password):
        """
        Verifies if a provided password matches the stored legacy hashed password.
        Legacy passwords are identified by a specific hash length (64 characters).
        The method retrieves the password setting, computes the hash for the
        provided password using a private method, and compares it with the stored
        hash to confirm verification.

        :param password: The plaintext password to verify.
        :type password: str

        :return: True if the password matches the stored legacy hash, False otherwise.
        :rtype: bool
        """
        try:
            setting = Settings.get_or_none(name="password")
            if setting and len(setting.value) == 64:  # Legacy hash length
                return setting.value == self._password_salt(password)
            return False
        except Exception as e:
            self.app.logger.error(f"Failed to verify legacy password: {e}")
            return False

    def _password_salt(self, password):
        """
        Hashes a given password by appending a predefined salt to it and then applying
        SHA-256 hashing. This function ensures that passwords are stored or handled
        securely by adding a level of obfuscation and securing password storage.

        :param self: The reference to the instance of the class.
        :param password: The plain text password to be salted and hashed.
        :type password: str
        :return: The SHA-256 hashed password as a hexadecimal string.
        :rtype: str
        """
        salt = "thesis-genius-salt"
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
