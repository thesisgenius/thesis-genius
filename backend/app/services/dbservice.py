import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from backend import Settings, database_proxy


class DBService:
    def __init__(self, app, setting_keys=None):
        self.db = database_proxy
        self.app = app
        self.setting_keys = setting_keys or ["user", "email", "debug_mode"]

    def connect(self):
        """
        Establish a connection to the database.
        """
        if self.db.is_closed():
            self.db.connect()
            self.app.logger.info("Database connection established.")

    def close_connection(self):
        """
        Close the database connection if open.
        """
        if not self.db.is_closed():
            self.db.close()
            self.app.logger.info("Database connection closed.")

    def is_initialized(self):
        """
        Check if the database is initialized by verifying the existence of the Settings table.
        """
        return Settings.table_exists()

    def initialize(self):
        """
        Create database tables if they do not exist.
        """
        from backend import User, Theses, Post, Settings
        with self.db:
            self.db.create_tables([User, Theses, Post, Settings], safe=True)

    def load_settings(self):
        """
        Load application settings into Flask app config.
        """
        from backend import Settings
        setting_keys = ["user", "email", "debug_mode"]
        for name in setting_keys:
            setting = Settings.get_or_none(name=name)
            self.app.config[name] = setting.value if setting else ""

    def save_settings(self, settings_dict):
        """
        Save application settings to the database.
        """
        try:
            for name in self.setting_keys:
                value = settings_dict.get(name, "")
                setting, created = Settings.get_or_create(name=name)
                setting.value = value
                setting.save()
            self.load_settings()  # Refresh settings in the app config
            self.app.logger.info("Application settings saved successfully.")
        except Exception as err:
            self.app.logger.error(f"Failed to save settings: {err}")

    # Password Management
    def save_password(self, password):
        """
        Save a hashed password in the database.
        """
        try:
            setting, created = Settings.get_or_create(name="password")
            setting.value = generate_password_hash(password)
            setting.save()
            self.app.logger.info("Password saved successfully.")
        except Exception as err:
            self.app.logger.error(f"Failed to save password: {err}")

    def check_password(self, password):
        """
        Check the provided password against the stored hashed password.
        """
        try:
            setting = Settings.get_or_none(name="password")
            if setting and setting.value:
                return check_password_hash(setting.value, password)
            self.app.logger.warning("Password not found.")
            return False
        except Exception as err:
            self.app.logger.error(f"Failed to check password: {err}")
            return False

    def _password_salt(self, password):
        """
        Generate a salted hash of the password for backward compatibility.
        """
        salt = "thesis-genius-salt"
        return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()

    def verify_legacy_password(self, password):
        """
        Check passwords hashed using the legacy _password_salt method.
        """
        try:
            setting = Settings.get_or_none(name="password")
            if setting and len(setting.value) == 64:
                # Legacy salted hash
                return setting.value == self._password_salt(password)
            return False
        except Exception as err:
            self.app.logger.error(f"Failed to verify legacy password: {err}")
            return False
