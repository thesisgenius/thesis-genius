import jwt
from functools import wraps
from flask import current_app, g, jsonify, request
from datetime import datetime, timedelta, timezone
from backend import UserService

user_service = UserService()

def generate_token(user_id):
    """Generate a JWT token."""
    payload = {
        "user_id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Token expires in 1 hour
    }
    secret_key = current_app.config["SECRET_KEY"]  # Access SECRET_KEY within the function
    return jwt.encode(payload, secret_key, algorithm="HS256")


def validate_token(token):
    """Validate a JWT token."""
    try:
        secret_key = current_app.config["SECRET_KEY"]  # Access SECRET_KEY within the function
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
            current_app.logger.error("JWT missing in request")
            return jsonify({"success": False, "message": "Token is missing"}), 401

        try:
            secret_key = current_app.config["SECRET_KEY"]
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user_id = payload["user_id"]
            current_app.logger.info(f"User ID {g.user_id} authenticated")
        except jwt.ExpiredSignatureError:
            current_app.logger.error("JWT token has expired")
            return jsonify({"success": False, "message": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            current_app.logger.error("JWT token is invalid")
            return jsonify({"success": False, "message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function



def load_user():
    """
    Middleware to load the user object into the Flask `g` context.
    Fetches user data from the database based on `g.user_id`.
    """
    if hasattr(g, "user_id"):
        user = user_service.get_user_data(g.user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        g.user = user
