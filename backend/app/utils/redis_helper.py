import redis
from flask import current_app as app

def get_redis_client():
    """
    Lazily initialize and return a Redis client.
    """
    redis_connection_info = app.config.get("REDIS_CONNECTION_INFO", {})
    return redis.StrictRedis(
        host=redis_connection_info.get("host", "localhost"),
        port=redis_connection_info.get("port", 6379),
        db=redis_connection_info.get("db", 0),
        password=redis_connection_info.get("password", None),
        decode_responses=True,
    )

def blacklist_token(token):
    """
    Add a JWT token to Redis with an expiration time.
    """
    redis_client = get_redis_client()
    ttls_seconds = 3600
    redis_client.setex(f"blacklist:{token}", ttls_seconds, "true")

def is_token_blacklisted(token):
    """
    Check if a token exists in the Redis blacklist.
    """
    redis_client = get_redis_client()
    return redis_client.exists(f"blacklist:{token}") > 0
