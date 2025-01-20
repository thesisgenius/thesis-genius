from datetime import datetime, timezone

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
            # Generate a new JWT token
            token = user_service.generate_token(user["id"])

            # Log login details
            app.logger.info(
                f"User {user['id']} logged in successfully at {datetime.now(timezone.utc)}"
            )

            # Return token to client
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

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        institution = data.get("institution")
        password = data.get("password")
        role = data.get("role", "Student")
        is_active = True

        if not first_name or not last_name or not email or not password:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "First name, last name, email, and password are required",
                    }
                ),
                400,
            )

        success = user_service.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            institution=institution,
            password=password,
            role=role,
            is_active=is_active,
        )
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
