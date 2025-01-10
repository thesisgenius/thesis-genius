from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app as app
from flask import g, jsonify, request


def generate_token(user_id):
    """
    Generate a JWT token for the given user ID.
    """
    try:
        payload = {
            "user_id": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")
        return token
    except Exception as e:
        app.logger.error(f"Failed to generate token for user {user_id}: {e}")
        return None

def validate_token(token):
    """Validate a JWT token."""
    try:
        secret_key = app.config["SECRET_KEY"]  # Access SECRET_KEY within the function
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            app.logger.error("JWT missing in request")
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            from ..utils.redis_helper import is_token_blacklisted
            if is_token_blacklisted(token):
                return jsonify({"success": False, "message": "Token is expired and blacklisted"}), 401
            secret_key = app.config["SECRET_KEY"]
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user_id = payload["user_id"]
            app.logger.info(f"User ID {g.user_id} authenticated")
        except jwt.ExpiredSignatureError:
            app.logger.error("JWT token has expired")
            return jsonify({"success": False, "message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            app.logger.error("JWT token is invalid")
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function

def admin_required(f):
    """
    Middleware to ensure the user has admin privileges.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user_id:
            return jsonify({"success": False, "message": "Unauthorized"}), 401

        # Check if the user is an admin
        from ..models.data import User
        user = User.get_or_none(User.id == g.user_id)
        if not user or not user.is_admin:
            return jsonify({"success": False, "message": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated_function


def load_user():
    """
    Middleware to load the user object into the Flask `g` context.
    Fetches user data from the database based on `g.user_id`.
    """
    from ..services.userservice import UserService

    user_service = UserService(app.logger)
    if hasattr(g, "user_id"):
        user = user_service.get_user_data(g.user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        g.user = user
