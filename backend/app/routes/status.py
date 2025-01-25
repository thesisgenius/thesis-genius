from flask import Blueprint, jsonify

status_bp = Blueprint("status", __name__, url_prefix="/api/status")


@status_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health Check Endpoint
    Returns a basic 200 OK response to indicate the app is running.
    """
    return jsonify({"status": "healthy"}), 200


@status_bp.route("/ready", methods=["GET"])
def readiness_check():
    """
    Readiness Check Endpoint
    Ensures that the app's dependencies are ready.
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
            500,
        )

    except PeeweeException as pe:
        return (
            jsonify(
                {"status": "unready", "error": "Database Error", "details": str(pe)}
            ),
            500,
        )

    except Exception as e:
        return (
            jsonify({"status": "unready", "error": "Unknown Error", "details": str(e)}),
            500,
        )
