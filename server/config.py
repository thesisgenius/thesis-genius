import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    FLASK_PORT = os.getenv("FLASK_PORT", 5000)
    FLASK_APP = os.getenv("FLASK_APP", "server.app:create_app")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL",
        "mysql+pymysql://thesis_dev:dev_password@localhost/thesis_app_dev",
    )
    DEBUG = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://prod_user:prod_password@cloud-mysql-url/prod_db",
    )
    DEBUG = False


config_dict = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
