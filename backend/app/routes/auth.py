from datetime import datetime, timezone

from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request
from peewee import IntegrityError

from ..services.userservice import UserService
from ..utils.auth import jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signin", methods=["POST"])
def signin():
    """
    Handles user sign-in requests by authenticating the user credentials. Checks the
    presence of required fields in the request body, validates user credentials via
    the UserService, and generates a JWT token upon successful authentication. Logs
    successful logins and errors.

    :raises KeyError: If the data dictionary is missing required keys (email or password).
    :raises Exception: For any generic errors during the sign-in process.

    :return: A JSON response containing success status, token on successful authentication,
             or error messages with appropriate HTTP status codes.
    :rtype: tuple
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
    Handles the user registration process by validating input data, creating a new user,
    and returning appropriate HTTP responses. The function ensures all required fields
    are provided and valid, processes the user creation logic, and handles potential
    errors such as database integrity violations or unexpected exceptions.

    :raises IntegrityError: If the email or username violates unique constraints in the database.
    :raises ValueError: For validation errors that occur during user creation.

    :returns: JSON response indicating the success or failure of the registration process along
        with an appropriate HTTP status code.
    :rtype: Tuple[flask.Response, int]
    """
    # Instantiate the UserService
    user_service = UserService(app.logger)
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Missing request body"}), 400

        # Validate required fields before proceeding
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        institution = data.get("institution")

        if not all([first_name, last_name, email, password, institution]):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "First name, last name, email, institution and password are required",
                    }
                ),
                400,
            )

        # Set username to email prefix if not provided
        username = data.get("username", email.split("@")[0])
        role = data.get("role", "Student")
        is_active = True

        success = user_service.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
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
    except IntegrityError:
        # Handle uniqueness constraint error
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Email might already be in use or username is not unique.",
                }
            ),
            409,
        )

    except ValueError as e:
        app.logger.error(f"Validation error during user creation: {e}")
        return jsonify({"success": False, "message": str(e)}), 400

    except Exception as e:
        # Log the error and return a 500 for unexpected cases
        app.logger.error(f"Error during registration: {e}")
        return (
            jsonify(
                {
                    "success": False,
                    "message": "Internal Server Error. Please try again later.",
                }
            ),
            500,
        )


@auth_bp.route("/signout", methods=["POST"])
@jwt_required
def signout():
    """
    Handles the user sign-out process. This route requires the caller to be authenticated
    using JWT. It extracts the user ID from the request context and the token from the
    Authorization header, then delegates the logout process to the UserService. Returns a
    JSON response indicating the success or failure of the logout process.

    :raises Exception: If an unexpected error occurs during the sign-out process.

    :return: A `flask.Response` object containing a JSON payload indicating success or failure
             and an HTTP status code. The possible status codes are 200 for a successful logout,
             400 if the token is missing or logout fails, and 500 for internal errors.
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
