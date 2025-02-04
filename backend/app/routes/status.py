from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__, url_prefix="/api/status")


@status_bp.route("/health", methods=["GET"])
def health_check():
    """
    Performs a health check for the application by verifying system resource usage,
    validating environment-specific variables, and assessing the runtime environment.
    The function determines the health status of the application and reports any
    issues detected during the check.

    :return: If all checks pass, returns a JSON response indicating
        a healthy status with the current environment and a 200 HTTP status code.
        If any check fails, returns a JSON response with unhealthy status,
        corresponding error details, and the appropriate HTTP status code.
    :rtype: flask.Response
    :raises: Returns 503 HTTP status code if memory usage or CPU usage exceeds
        predefined limits, required environment variables are missing, or
        the FLASK_ENV variable has an invalid value. Returns 500 HTTP status
        code for unexpected errors.
    """
    import os

    import psutil  # For system-level resource checks

    try:
        # Check memory usage
        memory_info = psutil.virtual_memory()
        if memory_info.percent > 85:
            return jsonify({"status": "unhealthy", "error": "High memory usage"}), 503

        # Check CPU usage
        cpu_usage = psutil.cpu_percent(interval=0.5)
        if cpu_usage > 90:
            return jsonify({"status": "unhealthy", "error": "High CPU usage"}), 503

        # Environment-specific checks
        flask_env = os.getenv("FLASK_ENV", "development")

        if flask_env == "development":
            required_env_vars = [
                "DEV_DATABASE_ENGINE",
                "DEV_DATABASE_NAME",
                "DEV_DATABASE_USER",
                "DEV_DATABASE_PASSWORD",
                "DEV_DATABASE_HOST",
            ]
        elif flask_env == "testing":
            required_env_vars = [
                "TEST_DATABASE_ENGINE",
                "TEST_DATABASE_NAME",
            ]
        elif flask_env == "production":
            required_env_vars = [
                "PROD_DATABASE_ENGINE",
                "PROD_DATABASE_NAME",
                "PROD_DATABASE_USER",
                "PROD_DATABASE_PASSWORD",
                "PROD_DATABASE_HOST",
            ]
        else:
            return (
                jsonify({"status": "unhealthy", "error": "Unknown FLASK_ENV value"}),
                503,
            )

        # Validate environment variables
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_env_vars:
            return (
                jsonify(
                    {
                        "status": "unhealthy",
                        "error": "Missing required environment variables",
                        "details": missing_env_vars,
                    }
                ),
                503,
            )

        # If all checks pass
        return jsonify({"status": "healthy", "environment": flask_env}), 200

    except Exception as e:
        return (
            jsonify(
                {"status": "unhealthy", "error": "Unknown error", "details": str(e)}
            ),
            500,
        )


@status_bp.route("/ready", methods=["GET"])
def readiness_check():
    """
    Determines the readiness of the application for handling requests by performing checks
    against critical components, including the database and Redis cache. The endpoint
    returns an appropriate HTTP status code and a JSON response depending on the readiness
    status of the application.

    An HTTP 200 response with `{"status": "ready"}` indicates that all system dependencies
    are fully operational. Otherwise, error information is returned alongside the HTTP
    status code, signaling the system's unready state and specific dependency failures.

    :raises redis.exceptions.RedisError: Raised if Redis is unreachable or responds with an error.
    :raises PeeweeException: Raised if the database connection or query execution fails.
    :raises Exception: Raised if an unknown error occurs during the readiness check.

    :return: Tuple containing a JSON response object with readiness status and HTTP status code.
    :rtype: tuple
    """
    import redis
    from peewee import PeeweeException

    from ..utils.db import database_proxy
    from ..utils.redis_helper import get_redis_client

    try:
        # Example: Check database connection
        if database_proxy.is_closed():
            database_proxy.connect()
        database_proxy.execute_sql(
            "SELECT 1"
        )  # A simple query to validate DB connection

        # Check Redis connection
        redis_client = get_redis_client()
        redis_client.ping()  # Simple command to validate Redis connection

        return jsonify({"status": "ready"}), 200
    except redis.exceptions.RedisError as re:
        return (
            jsonify({"status": "unready", "error": "Redis Error", "details": str(re)}),
            503,
        )

    except PeeweeException as pe:
        return (
            jsonify(
                {"status": "unready", "error": "Database Error", "details": str(pe)}
            ),
            503,
        )

    except Exception as e:
        return (
            jsonify({"status": "unready", "error": "Unknown Error", "details": str(e)}),
            500,
        )


@status_bp.route("/alive", methods=["GET"])
def alive_check():
    """
    Handles health check endpoint to verify if the service is running and operational.

    This endpoint responds with a simple status message to inform that the service
    is alive and accessible. It is typically used by monitoring systems or other
    services to ensure the availability of this application.

    :return: A JSON response containing the status message and an HTTP status code.

    :rtype: Tuple[dict, int]
    """
    return jsonify({"status": "alive"}), 200
