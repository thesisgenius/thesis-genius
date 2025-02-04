import os


class Config:
    """
    Configuration class for the application.

    This class provides configuration variables used by the application. It includes
    settings such as secret keys, application specific configurations, debugging and
    testing flags, and connections for the database and Redis. The values are often
    retrieved from environment variables, making it easier to adjust configurations
    without modifying the codebase.

    :ivar SECRET_KEY: Secret key for application security, typically used for session
        management or encryption purposes.
    :type SECRET_KEY: str
    :ivar FLASK_PORT: Port on which the Flask application runs.
    :type FLASK_PORT: int
    :ivar FLASK_APP: Location and creation entry point for the Flask app.
    :type FLASK_APP: str
    :ivar DEBUG: Debug mode flag for the application.
    :type DEBUG: bool
    :ivar TESTING: Testing mode flag for the application.
    :type TESTING: bool
    :ivar DB_CONNECTION_INFO: Dictionary containing configuration settings for the
        Peewee database connection, including name, engine, user, password, host,
        and port.
    :type DB_CONNECTION_INFO: dict
    :ivar REDIS_CONNECTION_INFO: Dictionary containing configuration settings for
        the Redis connection, including host, port, and database index.
    :type REDIS_CONNECTION_INFO: dict
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    FLASK_PORT = os.getenv("FLASK_PORT", 5000)
    FLASK_APP = os.getenv("FLASK_APP", "backend.app:create_app")
    DEBUG = False
    TESTING = False
    # Peewee Database Configuration (default to test connection)
    DB_CONNECTION_INFO = {
        "name": os.getenv("TEST_DATABASE_NAME", ":memory:"),
        "engine": "sqlite",  # Use SQLite for in-memory testing
        "user": None,
        "password": None,
        "host": None,
        "port": None,
    }
    REDIS_CONNECTION_INFO = {
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }


class DevelopmentConfig(Config):
    """
    Configuration class for the development environment.

    This class is designed to manage and store configuration settings specific to the
    development environment of the application. It includes database connection details
    and other environment-related settings.

    :ivar DB_CONNECTION_INFO: Contains the database connection details such as name,
        engine, user, password, host, and port for the development environment.
    :type DB_CONNECTION_INFO: dict
    :ivar DEBUG: Indicates whether the debug mode is enabled in the development environment.
    :type DEBUG: bool
    """

    DB_CONNECTION_INFO = {
        "name": os.getenv("DEV_DATABASE_NAME", "thesis_app_dev"),
        "engine": os.getenv("DEV_DATABASE_ENGINE", "mysql"),
        "user": os.getenv("DEV_DATABASE_USER", "thesis_dev"),
        "password": os.getenv("DEV_DATABASE_PASSWORD", "dev_password"),
        "host": os.getenv("DEV_DATABASE_HOST", "localhost"),
        "port": 3306,
    }
    DEBUG = True


class TestingConfig(Config):
    """
    Testing configuration class for setting up and managing configurations needed for
    unit tests and other test environments.

    This class inherits from the `Config` base class and customizes settings specifically
    required for testing scenarios. These configurations include connection information
    to a test database, and enabling the testing mode flag, among others.

    :ivar DB_CONNECTION_INFO: Information related to test database connectivity,
        such as database name, engine, user, password, host, and port.
    :type DB_CONNECTION_INFO: dict
    :ivar TESTING: Flag to indicate the application is in testing mode.
    :type TESTING: bool
    """

    DB_CONNECTION_INFO = {
        "name": os.getenv("TEST_DATABASE_NAME", ":memory:"),
        "engine": os.getenv(
            "TEST_DATABASE_ENGINE", "sqlite"
        ),  # Use SQLite for in-memory testing
        "user": None,
        "password": None,
        "host": None,
        "port": None,
    }
    TESTING = True


class ProductionConfig(Config):
    """
    ProductionConfig class for managing production-level configuration settings.

    This class is used to define and manage production-specific configuration
    values for an application. It includes database connection settings and
    controls specific to the production environment.

    :ivar MYSQL_CONFIG: Dictionary containing the production database configuration
                        details such as name, engine, user, password, host, and port.
    :type MYSQL_CONFIG: dict
    :ivar DEBUG: Flag indicating whether debug mode is enabled. For production,
                 this is set to False.
    :type DEBUG: bool
    """

    MYSQL_CONFIG = {
        "name": os.getenv("PROD_DATABASE_NAME", "prod_db"),
        "engine": os.getenv("PROD_DATABASE_ENGINE", "mysql"),
        "user": os.getenv("PROD_DATABASE_USER", "prod_user"),
        "password": os.getenv("PROD_DATABASE_PASSWORD", "prod_password"),
        "host": os.getenv("PROD_DATABASE_HOST", "cloud-mysql-url"),
        "port": int(os.getenv("PROD_DATABASE_PORT", 3306)),
    }
    DEBUG = False


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
