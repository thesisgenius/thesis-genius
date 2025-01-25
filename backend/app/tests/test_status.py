import pytest
from unittest.mock import patch


@pytest.fixture
def mock_env(monkeypatch):
    """
    Fixture to mock environment variables for testing.
    """
    def set_env(env_vars):
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

    return set_env


def test_status_health_ok(client, mock_env):
    """
    Test the /api/status/health endpoint when everything is healthy.
    """
    mock_env({
        "FLASK_ENV": "development",
        "DEV_DATABASE_ENGINE": "mysql",
        "DEV_DATABASE_NAME": "thesis_app_dev",
        "DEV_DATABASE_USER": "thesis_dev",
        "DEV_DATABASE_PASSWORD": "dev_password",
        "DEV_DATABASE_HOST": "localhost"
    })

    with patch("psutil.virtual_memory") as mock_memory, \
            patch("psutil.cpu_percent") as mock_cpu:
        mock_memory.return_value = type("svmem", (object,), {"percent": 12.5})
        mock_cpu.return_value = 25

        response = client.get("/api/status/health")
        assert response.status_code == 200
        assert response.json["status"] == "healthy"
        assert response.json["environment"] == "development"


def test_status_health_high_memory(client, mock_env):
    """
    Test the /api/status/health endpoint with high memory usage.
    """
    mock_env({
        "FLASK_ENV": "production",
        "PROD_DATABASE_ENGINE": "mysql",
        "PROD_DATABASE_NAME": "prod_db",
        "PROD_DATABASE_USER": "prod_user",
        "PROD_DATABASE_PASSWORD": "prod_password",
        "PROD_DATABASE_HOST": "cloud-mysql-url"
    })

    with patch("psutil.virtual_memory") as mock_memory, \
            patch("psutil.cpu_percent") as mock_cpu:
        mock_memory.return_value = type("svmem", (object,), {"percent": 93.75})
        mock_cpu.return_value = 25

        response = client.get("/api/status/health")
        assert response.status_code == 503
        assert response.json["status"] == "unhealthy"
        assert response.json["error"] == "High memory usage"


def test_status_health_high_cpu(client, mock_env):
    """
    Test the /api/status/health endpoint with high CPU usage.
    """
    mock_env({
        "FLASK_ENV": "production",
        "PROD_DATABASE_ENGINE": "mysql",
        "PROD_DATABASE_NAME": "prod_db",
        "PROD_DATABASE_USER": "prod_user",
        "PROD_DATABASE_PASSWORD": "prod_password",
        "PROD_DATABASE_HOST": "cloud-mysql-url"
    })

    with patch("psutil.virtual_memory") as mock_memory, \
            patch("psutil.cpu_percent") as mock_cpu:
        mock_memory.return_value = type("svmem", (object,), {"percent": 12.5})
        mock_cpu.return_value = 95

        response = client.get("/api/status/health")
        assert response.status_code == 503
        assert response.json["status"] == "unhealthy"
        assert response.json["error"] == "High CPU usage"


def test_status_health_missing_env_vars(client, mock_env):
    """
    Test the /api/status/health endpoint with missing environment variables.
    """
    mock_env({
        "FLASK_ENV": "testing",
        "TEST_DATABASE_ENGINE": "sqlite"
        # Missing TEST_DATABASE_NAME
    })

    with patch("psutil.virtual_memory") as mock_memory, \
            patch("psutil.cpu_percent") as mock_cpu:
        mock_memory.return_value = type("svmem", (object,), {"percent": 12.5})
        mock_cpu.return_value = 25

        response = client.get("/api/status/health")
        assert response.status_code == 503
        assert response.json["status"] == "unhealthy"
        assert response.json["error"] == "Missing required environment variables"
        assert "TEST_DATABASE_NAME" in response.json["details"]


def test_status_alive_ok(client):
    """
    Test the /api/status/alive endpoint when the application is alive.
    """
    response = client.get("/api/status/alive")
    assert response.status_code == 200
    assert response.json["status"] == "alive"
