from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.userservice import UserService
from ..utils.auth import jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signin", methods=["POST"])
def signin():
    """
    API endpoint for user sign-in.
    """
    # Instantiate the UserService
    user_service = UserService(app.logger)
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Missing request body"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return (
                jsonify(
                    {"success": False, "message": "Email and password are required"}
                ),
                400,
            )

        user = user_service.authenticate_user(email=email, password=password)
        if user:
            token = user_service.generate_token(user["id"])
            return jsonify({"success": True, "token": token}), 200

        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        app.logger.error(f"Error during sign-in: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    API endpoint for user registration.
    """
    # Instantiate the UserService
    user_service = UserService(app.logger)
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Missing request body"}), 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Name, email, and password are required",
                    }
                ),
                400,
            )

        success = user_service.create_user(name=name, email=email, password=password)
        if success:
            return (
                jsonify({"success": True, "message": "User registered successfully"}),
                201,
            )

        return (
            jsonify(
                {
                    "success": False,
                    "message": "Registration failed. Email might already be in use",
                }
            ),
            400,
        )
    except Exception as e:
        app.logger.error(f"Error during registration: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@auth_bp.route("/signout", methods=["POST"])
@jwt_required
def signout():
    """
    API endpoint for user sign-out.
    """
    # Instantiate the UserService
    user_service = UserService(app.logger)
    try:
        # Extract user ID and token from the context
        user_id = g.user_id
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 400

        # Call the logout method
        success = user_service.logout(user_id, token)
        if success:
            return jsonify({"success": True, "message": "Logged out successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to log out"}), 400
    except Exception as e:
        app.logger.error(f"Error during sign-out: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500

