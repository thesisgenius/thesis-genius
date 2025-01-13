from backend.app.config import (DevelopmentConfig, ProductionConfig,
                                TestingConfig)


def test_development_config(monkeypatch):
    """
    Test the DevelopmentConfig class.
    """
    monkeypatch.setenv("DEV_DATABASE_NAME", "dev_db")
    monkeypatch.setenv("DEV_DATABASE_ENGINE", "mysql")
    monkeypatch.setenv("DEV_DATABASE_USER", "dev_user")
    monkeypatch.setenv("DEV_DATABASE_PASSWORD", "dev_password")
    monkeypatch.setenv("DEV_DATABASE_HOST", "localhost")

    config = DevelopmentConfig()
    assert config.DEBUG is True
    assert config.DB_CONNECTION_INFO["name"] == "thesis_app_dev"
    assert config.DB_CONNECTION_INFO["engine"] == "mysql"
    assert config.DB_CONNECTION_INFO["user"] == "thesis_dev"
    assert config.DB_CONNECTION_INFO["password"] == "dev_password"
    assert config.DB_CONNECTION_INFO["host"] == "localhost"
    assert config.DB_CONNECTION_INFO["port"] == 3306


def test_testing_config(monkeypatch):
    """
    Test the TestingConfig class.
    """
    monkeypatch.setenv("TEST_DATABASE_NAME", "test_db")
    monkeypatch.setenv("TEST_DATABASE_ENGINE", "sqlite")

    config = TestingConfig()
    assert config.TESTING is True
    assert config.DB_CONNECTION_INFO["name"] == ":memory:"
    assert config.DB_CONNECTION_INFO["engine"] == "sqlite"
    assert config.DB_CONNECTION_INFO["user"] is None
    assert config.DB_CONNECTION_INFO["password"] is None
    assert config.DB_CONNECTION_INFO["host"] is None
    assert config.DB_CONNECTION_INFO["port"] is None


def test_production_config(monkeypatch):
    """
    Test the ProductionConfig class.
    """
    monkeypatch.setenv("PROD_DATABASE_NAME", "prod_db")
    monkeypatch.setenv("PROD_DATABASE_ENGINE", "mysql")
    monkeypatch.setenv("PROD_DATABASE_USER", "prod_user")
    monkeypatch.setenv("PROD_DATABASE_PASSWORD", "prod_password")
    monkeypatch.setenv("PROD_DATABASE_HOST", "cloud-mysql-url")
    monkeypatch.setenv("PROD_DATABASE_PORT", "3306")

    config = ProductionConfig()
    assert config.DEBUG is False
    assert config.MYSQL_CONFIG["name"] == "prod_db"
    assert config.MYSQL_CONFIG["engine"] == "mysql"
    assert config.MYSQL_CONFIG["user"] == "prod_user"
    assert config.MYSQL_CONFIG["password"] == "prod_password"
    assert config.MYSQL_CONFIG["host"] == "cloud-mysql-url"
    assert config.MYSQL_CONFIG["port"] == 3306


def test_default_config(monkeypatch):
    """
    Test default values for Config class.
    """
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("FLASK_PORT", raising=False)
    monkeypatch.delenv("FLASK_APP", raising=False)

    config = DevelopmentConfig()  # Any subclass can inherit defaults from Config
    assert config.SECRET_KEY == "dev"
    assert config.FLASK_PORT == 5000
    assert config.FLASK_APP == "backend.app:create_app"


def test_redis_config():
    """
    Test Redis configuration.
    """
    config = DevelopmentConfig()  # All environments inherit this
    redis_info = config.REDIS_CONNECTION_INFO

    assert redis_info["host"] == "localhost"
    assert redis_info["port"] == 6379
    assert redis_info["db"] == 0
