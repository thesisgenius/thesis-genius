from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app as app
from flask import g, jsonify, request

from ..utils.redis_helper import add_token_to_user, is_token_blacklisted


def generate_token(user_id):
    """
    Generates a JWT token for a user, adds it to Redis for tracking, and sets an expiry time.

    This method creates a JSON Web Token (JWT) containing the user ID, its expiration
    time (set to 1 hour from the current time), and the issued-at time.
    The token is then encoded with the application's secret key and "HS256" algorithm,
    added to the Redis store with an expiry of one hour before being returned.

    :param user_id: An identifier for the user for whom the token is being generated.
    :type user_id: str
    :return: A JWT token representing the user's session.
    :rtype: str
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

    # Add token to Redis
    expiry_seconds = 3600  # 1 hour
    add_token_to_user(user_id, token, expiry_seconds)
    return token


def validate_token(token):
    """
    Validates a JWT token and retrieves the user ID from it. This function decodes the token
    using the secret key configured in the application's settings and ensures it adheres
    to the HS256 algorithm. If the token is invalid or expired, the function gracefully handles
    these cases, returning None without disturbing the application flow.

    :param token: A JSON Web Token (JWT) string that is to be verified and decoded.
    :type token: str
    :return: The user ID extracted from the token if the token is valid and contains it;
        otherwise, None in the case of expired or invalid tokens.
    :rtype: str or None
    """
    try:
        secret_key = app.config["SECRET_KEY"]  # Access SECRET_KEY within the function
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    """
    A decorator function to enforce JWT-based authentication on API endpoints.

    This function wraps around an endpoint view function and ensures that an
    authorization header with a valid JWT token is included in the request.
    The token is validated for format, expiration, potential blacklisting,
    and decoding using the application's secret key. If the token passes all
    checks, the user ID extracted from the token's payload is stored in the
    global `g` context for downstream processing.

    The decorator handles error cases such as a missing or malformed header,
    missing or blacklisted tokens, expired tokens, and invalid tokens,
    and returns appropriate JSON responses with a 401 status.

    :param f: The endpoint function to be wrapped by the decorator.
    :returns: The decorated function with JWT enforcement applied.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            app.logger.error("Authorization header is missing or malformed")
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Authorization header must start with 'Bearer'",
                    }
                ),
                401,
            )

        token = auth_header.replace("Bearer ", "")
        if not token:
            app.logger.error("JWT token is missing in request")
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            # Check if token is blacklisted
            if is_token_blacklisted(token):
                app.logger.error("JWT token is blacklisted")
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "Token is expired and blacklisted",
                        }
                    ),
                    401,
                )

            # Decode the JWT token
            secret_key = app.config["SECRET_KEY"]
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user_id = payload["user_id"]
            app.logger.info(f"User ID {g.user_id} authenticated")
        except jwt.ExpiredSignatureError:
            app.logger.error("JWT token has expired")
            return jsonify({"success": False, "message": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            app.logger.error(f"JWT token is invalid: {str(e)}")
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):
    """
    This function is a decorator that ensures the decorated route or function is
    accessible only to users with admin privileges in the system. It performs
    the necessary checks to validate whether the request is coming from a logged-in
    user with administrative rights, and appropriately denies access or allows
    the request to proceed.

    :param f: The function to be decorated.
    :type f: Callable

    :return: The original function wrapped with additional checks for admin access.
    :rtype: Callable

    :raises UnauthorizedException: Raised when the user is not logged in.
    :raises NotFoundException: Raised when the logged-in user's record is not
        found in the database.
    :raises ForbiddenException: Raised when the logged-in user lacks admin access.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user_id:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        # Check if the user is an admin
        from ..models.data import User

        user = User.get_or_none(User.id == g.user_id)
        if not user:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"User {user.first_name} (id:{user.id}) not found!",
                    }
                ),
                404,
            )
        if not user.is_admin:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": f"Admin access required (user {user.first_name}, id: {user.id})",
                    }
                ),
                403,
            )
        return f(*args, **kwargs)

    return decorated_function


def load_user():
    """
    Loads the current user based on the user_id stored in the global Flask object `g`.
    This function interacts with the `UserService` to retrieve user data using the
    `user_id`. If no user is found, it returns a JSON response indicating the
    failure and an HTTP 404 status code. If the user is successfully loaded, it is
    stored in the `g` object for further use within the request lifecycle.

    :return: A tuple containing a JSON response and an HTTP status code if the user
        is not found, otherwise no value is returned
    :rtype: tuple | None
    """
    from ..services.userservice import UserService

    user_service = UserService(app.logger)
    if hasattr(g, "user_id"):
        user = user_service.fetch_user_data(g.user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        g.user = user
