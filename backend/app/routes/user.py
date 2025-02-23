from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.userservice import UserService
from ..utils.auth import admin_required, jwt_required

user_bp = Blueprint("user_api", __name__, url_prefix="/api/user")

@user_bp.route("/profile-picture", methods=["POST"])
@jwt_required
def upload_profile_picture():
    """Endpoint to upload and update a user's profile picture."""
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        if "profile_picture" not in request.files:
            return jsonify({"success": False, "message": "No file uploaded"}), 400

        file = request.files["profile_picture"]
        response, status_code = user_service.update_profile_picture(user_id, file)
        return jsonify(response), status_code
    except Exception as e:
        app.logger.error(f"Error uploading profile picture: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500

@user_bp.route("/profile", methods=["GET"])
@jwt_required
def get_user_profile():
    """
    Handles the GET request to retrieve a user's profile information. The user's ID is
    retrieved from the global context (g), and user data is fetched using the UserService.
    If the user is not found, returns a 404 response. In case of an internal error, logs
    the error and returns a 500 response.

    :raises Exception: If an error occurs while fetching user profile data.
    :return: JSON response containing user profile data or an error message, along with the
        respective HTTP status code.
    :rtype: flask.Response
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        user_data = user_service.fetch_user_data(user_id)
        if not user_data:
            return jsonify({"success": False, "message": "User not found"}), 404

        return jsonify({"success": True, "user": user_data}), 200
    except Exception as e:
        app.logger.error(f"Error fetching user profile: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@user_bp.route("/profile", methods=["PUT"])
@jwt_required
def update_user_profile():
    """
    Updates the profile information of the currently authenticated user. The endpoint
    is protected with JWT and requires the user to be authenticated before access. It
    accepts a JSON payload with the user's first name, last name, and email, validates
    the input, and then updates the user's data via the `UserService`. If the payload
    or required fields are invalid, an appropriate error response is returned. In the
    case of success, the profile is updated, and a success response is sent back.

    :param: None.

    :raises JSONDecodeError: If the request payload is not valid JSON.
    :raises Exception: For general internal errors during execution.

    :return: A JSON response indicating success or failure along with an appropriate
        HTTP status code.
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Invalid payload"}), 400

        updated_data = {
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
        }

        if (
            not updated_data["first_name"]
            or not updated_data["last_name"]
            or not updated_data["email"]
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "First name, last name, and email are required",
                    }
                ),
                400,
            )

        success = user_service.update_user(user_id, updated_data)
        if success:
            return (
                jsonify({"success": True, "message": "Profile updated successfully"}),
                200,
            )

        return jsonify({"success": False, "message": "Failed to update profile"}), 400
    except Exception as e:
        app.logger.error(f"Error updating user profile: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@user_bp.route("/deactivate", methods=["PUT"])
@jwt_required
def deactivate_user():
    """
    Deactivates a user account by invoking the corresponding service method and verifies the
    request token from the headers. Logs errors and handles potential exceptions. Returns appropriate
    response based on success or failure of the deactivation process.

    :raises Exception: If any unexpected error occurs during user account deactivation.
    :rtype: flask.Response
    :return: Returns a JSON response with a success or failure message. Response status code
             is 200 if the user account is successfully deactivated, otherwise 400 for client
             errors or 500 for server errors.
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 400
        success = user_service.update_user(user_id, token)
        if success:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "User account deactivated successfully",
                    }
                ),
                200,
            )
        return (
            jsonify({"success": False, "message": "Failed to deactivate user account"}),
            400,
        )
    except Exception as e:
        app.logger.error(f"Error deactivating user account: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@user_bp.route("/activate/<int:user_id>", methods=["PUT"])
@jwt_required
@admin_required
def activate_user(user_id):
    """
    Activate a user by changing their status to active. This endpoint requires users to be
    authenticated and have admin privileges. It uses the `change_user_status` method of the
    user service to update the user status and logs errors, if any, during the operation.
    A success or failure response is returned based on the operation's outcome.

    :param user_id: The ID of the user to be activated.
    :type user_id: int
    :return: A JSON response containing the success status and a message. Returns an HTTP
        status code of 200 if the operation succeeds, 400 if the user is already active or
        not found, and 500 in case of an unexpected server error.
    :rtype: tuple
    """
    user_service = UserService(app.logger)

    # Change user status using the `change_user_status` method
    try:
        success = user_service.change_user_status(user_id=user_id, is_active=True)
        if success:
            return (
                jsonify({"success": True, "message": "User activated successfully"}),
                200,
            )
        return (
            jsonify(
                {"success": False, "message": "User is already active or not found"}
            ),
            400,
        )
    except Exception as e:
        app.logger.error(f"Error activating user {user_id}: {e}")
        return jsonify({"success": False, "message": "Failed to activate user"}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_user(user_id):
    """
    Deletes and deactivates a user by their ID. The endpoint requires the user to have a valid JWT
    and admin privileges to perform the action. If the specified user is not found, a 404 error
    is returned. If the deactivation process is successful, a success message is returned with
    a 200 status code. Otherwise, an error message with a 500 status code is returned.

    :param user_id: ID of the user to be deactivated
    :type user_id: int
    :return: A JSON object containing a success or error message along with the corresponding
             HTTP status code
    :rtype: Tuple[Response, int]
    """
    user_service = UserService(app.logger)
    user = user_service.fetch_user_data(user_id)
    if not user:
        return jsonify({"error": f"User with ID {user_id} not found"}), 404

    success = user_service.update_user(user_id, {"is_active": False})
    if success:
        return jsonify({"message": f"User {user_id} deactivated successfully"}), 200
    return jsonify({"error": f"Failed to deactivate user {user_id}"}), 500
