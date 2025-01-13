import redis
from datetime import datetime, timezone, timedelta
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
def add_token_to_user(user_id, token, expiry_seconds):
    """
    Add a token to the user's token list in Redis.
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    expiry_time = (datetime.now(timezone.utc)+ timedelta(seconds=expiry_seconds)).timestamp()
    redis_client.hset(token_key, token, expiry_time)
    redis_client.expire(token_key, expiry_seconds)  # Expire user's token list after the longest token expires

def blacklist_token(token, ttl=3600):
    """
    Add a JWT token to Redis with an optional expiration time (default is 3600 seconds).
    """
    redis_client = get_redis_client()
    redis_client.setex(f"blacklist:{token}", ttl, "true")

def is_token_blacklisted(token):
    """
    Check if a token exists in the Redis blacklist.
    """
    redis_client = get_redis_client()
    return redis_client.exists(f"blacklist:{token}") > 0

def get_user_tokens(user_id):
    """
    Get all tokens issued to a specific user.
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    return redis_client.hgetall(token_key)

def revoke_user_tokens(user_id):
    """
    Revoke all tokens for a user by blacklisting them.
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    tokens = redis_client.hkeys(token_key)

    for token in tokens:
        # Redis keys/values may be byte strings; decode if necessary
        token_str = token if isinstance(token, str) else token.decode("utf-8")
        expiry = redis_client.hget(token_key, token_str)
        expiry = float(expiry) if isinstance(expiry, str) else float(expiry.decode("utf-8"))

        remaining_ttl = max(0, int(expiry - datetime.now(timezone.utc).timestamp()))
        blacklist_token(token_str, remaining_ttl)

    redis_client.delete(token_key)


def is_token_expired(token):
    """
    Check if a token is expired based on its tracked expiry.
    """
    redis_client = get_redis_client()
    expiry_key = f"token:{token}:expiry"
    expiry_timestamp = redis_client.get(expiry_key)
    if not expiry_timestamp:
        return True
    return datetime.now(timezone.utc).timestamp() > float(expiry_timestamp)