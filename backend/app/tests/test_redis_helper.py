from datetime import datetime, timedelta, timezone

from backend.app.utils.redis_helper import (add_token_to_user, blacklist_token,
                                            get_user_tokens,
                                            is_token_blacklisted,
                                            is_token_expired,
                                            revoke_user_tokens)


def test_add_token_to_user(mock_redis):
    """
    Test adding a token to a user's token list in Redis.
    """
    user_id = 1
    token = "test_token"
    expiry_seconds = 3600

    add_token_to_user(user_id, token, expiry_seconds)

    redis_client = mock_redis
    token_key = f"user:{user_id}:tokens"

    assert redis_client.hexists(token_key, token)
    expiry = redis_client.hget(token_key, token)
    assert float(expiry) > datetime.now(timezone.utc).timestamp()
    assert redis_client.ttl(token_key) == expiry_seconds


def test_blacklist_token(mock_redis):
    """
    Test blacklisting a token in Redis.
    """
    token = "blacklisted_token"
    ttl = 3600

    blacklist_token(token, ttl)

    redis_client = mock_redis
    assert redis_client.exists(f"blacklist:{token}")
    assert (redis_client.ttl(f"blacklist:{token}") > 0 <= ttl) is True


def test_is_token_blacklisted(mock_redis):
    """
    Test checking if a token is blacklisted.
    """
    token = "blacklisted_token"
    blacklist_token(token)

    assert is_token_blacklisted(token) is True
    assert is_token_blacklisted("non_blacklisted_token") is False


def test_get_user_tokens(mock_redis):
    """
    Test fetching all tokens issued to a user.
    """
    user_id = 1
    token1 = "token1"
    token2 = "token2"

    # Add tokens to Redis
    add_token_to_user(user_id, token1, 3600)
    add_token_to_user(user_id, token2, 3600)

    # Fetch tokens
    tokens = get_user_tokens(user_id)

    # Redis returns byte strings; convert keys to plain strings
    decoded_tokens = {key.decode("utf-8"): value for key, value in tokens.items()}
    assert len(decoded_tokens) == 2
    assert token1 in decoded_tokens
    assert token2 in decoded_tokens


def test_revoke_user_tokens(mock_redis):
    """
    Test revoking all tokens for a user.
    """
    user_id = 1
    token1 = "token1"
    token2 = "token2"

    # Add tokens to Redis
    add_token_to_user(user_id, token1, 3600)
    add_token_to_user(user_id, token2, 3600)

    # Assert tokens exist in the user's token list
    redis_client = mock_redis
    assert redis_client.hexists(f"user:{user_id}:tokens", token1) is True
    assert redis_client.hexists(f"user:{user_id}:tokens", token2) is True

    # Revoke all tokens
    revoke_user_tokens(user_id)
    token_key = f"user:{user_id}:tokens"

    # Verify the user's token list is deleted
    assert redis_client.exists(token_key) == 0

    # Verify the tokens are blacklisted
    blacklist_token_key1 = f"blacklist:{token1}"
    blacklist_token_key2 = f"blacklist:{token2}"

    assert redis_client.exists(blacklist_token_key1) == 1
    assert redis_client.exists(blacklist_token_key2) == 1
    assert is_token_blacklisted(token1) is True
    assert is_token_blacklisted(token2) is True


def test_is_token_expired(mock_redis):
    """
    Test checking if a token is expired.
    """
    token = "test_token"
    expiry_seconds = 3600
    expiry_timestamp = (
        datetime.now(timezone.utc) + timedelta(seconds=expiry_seconds)
    ).timestamp()

    redis_client = mock_redis
    redis_client.set(f"token:{token}:expiry", expiry_timestamp)

    assert is_token_expired(token) is False

    # Simulate expiration
    redis_client.set(
        f"token:{token}:expiry", datetime.now(timezone.utc).timestamp() - 10
    )
    assert is_token_expired(token) is True
