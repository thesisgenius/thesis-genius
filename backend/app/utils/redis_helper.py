from datetime import datetime, timedelta, timezone

import redis
from flask import current_app as app


def get_redis_client():
    """
    Creates and returns a Redis client configured with the connection details provided
    in the application configuration. If no specific connection details are provided,
    it defaults to localhost, port 6379, database 0, with no password. The client
    is configured to decode responses for convenience.

    :return: A Redis client instance configured based on application settings.
    :rtype: redis.StrictRedis
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
    Adds a token to the specified user in the Redis database with an associated expiry time.

    The function stores the provided token for a user in Redis using a hash structure
    and sets an expiry time for the user's token list to ensure it gets cleaned up after
    the token with the longest expiry duration is no longer valid. The `expiry_seconds`
    parameter defines how long the token and the list of the user's tokens remain valid.

    :param user_id: Identifier for the user to whom the token is added.
    :type user_id: str
    :param token: Unique token associated with the user.
    :type token: str
    :param expiry_seconds: The length of time in seconds until the token and token list expires.
    :type expiry_seconds: int
    :return: None
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    expiry_time = (
        datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
    ).timestamp()
    redis_client.hset(token_key, token, expiry_time)
    redis_client.expire(
        token_key, expiry_seconds
    )  # Expire user's token list after the longest token expires


def blacklist_token(token, ttl=3600):
    """
    Blacklist a given token in a Redis cache.

    This function takes a token and blacklists it by storing it in a Redis
    cache with a specified time-to-live (TTL). The token is no longer valid
    and should not be used further. An optional TTL parameter can be passed
    to override the default time-to-live period.

    :param token: The token to be blacklisted.
    :type token: str
    :param ttl: Time-to-live for the blacklisted token in seconds. Defaults
        to 3600 seconds if not specified.
    :type ttl: int, optional
    :return: None
    """
    redis_client = get_redis_client()
    redis_client.setex(f"blacklist:{token}", ttl, "true")


def is_token_blacklisted(token):
    """
    Checks whether a given token is blacklisted or not.

    This function connects to a Redis instance to check if the
    specific token exists in the blacklist. If the token exists
    in the blacklist, it is considered invalid or unauthorized.

    :param token: The token to be checked against the blacklist.
                  Must be a string representing the token.
    :returns: A boolean indicating whether the token is
              blacklisted (True if blacklisted, False otherwise).
    :rtype: bool
    """
    redis_client = get_redis_client()
    return redis_client.exists(f"blacklist:{token}") > 0


def get_user_tokens(user_id):
    """
    Retrieve all tokens associated with a specific user from Redis.

    This function queries the Redis database for all tokens linked to a given
    user ID. It uses a Redis hash structure where tokens are stored under a
    specific key pattern associated with the user. The retrieved tokens are
    returned as a dictionary.

    :param user_id: The unique identifier of the user for which tokens are
        being retrieved.
    :type user_id: str
    :return: A dictionary containing all tokens associated with the user,
        where the keys and values represent token attributes and their
        respective information.
    :rtype: dict
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    return redis_client.hgetall(token_key)


def revoke_user_tokens(user_id):
    """
    Revokes all tokens associated with a specified user by updating the token blacklist
    and removing the tokens from the Redis data store. This operation ensures that all
    access tokens linked to a user become invalid.

    The function iterates through tokens stored in Redis for the given user, calculates
    their remaining time-to-live (TTL), and adds them to a blacklist mechanism for
    validation during future requests. Once all tokens are processed, the function
    deletes the token entries in Redis.

    :param user_id: Unique identifier of the user whose tokens are to be revoked.
    :type user_id: str
    :return: None
    :rtype: NoneType
    """
    redis_client = get_redis_client()
    token_key = f"user:{user_id}:tokens"
    tokens = redis_client.hkeys(token_key)

    for token in tokens:
        # Redis keys/values may be byte strings; decode if necessary
        token_str = token if isinstance(token, str) else token.decode("utf-8")
        expiry = redis_client.hget(token_key, token_str)
        expiry = (
            float(expiry) if isinstance(expiry, str) else float(expiry.decode("utf-8"))
        )

        remaining_ttl = max(0, int(expiry - datetime.now(timezone.utc).timestamp()))
        blacklist_token(token_str, remaining_ttl)

    redis_client.delete(token_key)


def is_token_expired(token):
    """
    Checks if a provided token has expired by comparing the current timestamp with its expiry timestamp
    stored in a Redis cache.

    :param token: A string representing the token whose expiry is being verified.
    :type token: str
    :return: Returns True if the token has expired or if the expiry timestamp is not found;
        otherwise, returns False.
    :rtype: bool
    """
    redis_client = get_redis_client()
    expiry_key = f"token:{token}:expiry"
    expiry_timestamp = redis_client.get(expiry_key)
    if not expiry_timestamp:
        return True
    return datetime.now(timezone.utc).timestamp() > float(expiry_timestamp)
