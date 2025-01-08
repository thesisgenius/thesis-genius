import os


class Config:
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


class DevelopmentConfig(Config):
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
