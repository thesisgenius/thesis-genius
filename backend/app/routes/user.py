from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.userservice import UserService
from ..utils.auth import admin_required, jwt_required

user_bp = Blueprint("user_api", __name__, url_prefix="/api/user")


@user_bp.route("/profile", methods=["GET"])
@jwt_required
def get_user_profile():
    """
    Fetch the authenticated user's profile data.
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        user_data = user_service.get_user_data(user_id)
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
    Update the authenticated user's profile data.
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

        success = user_service.update_user_data(user_id, updated_data)
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
    Deactivate the authenticated user's account.
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        token = request.headers.get("Authorization", "").replace("Bearer ", "")

        if not token:
            return jsonify({"success": False, "message": "Token is missing"}), 400
        success = user_service.deactivate_user(user_id, token)
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
    Allow an admin to activate a user's account.
    """
    user_service = UserService(app.logger)
    target_user = user_service.get_user_data(user_id)

    if not target_user or target_user["is_active"]:
        return (
            jsonify(
                {"success": False, "message": "User is already active or not found"}
            ),
            400,
        )

    success = user_service.activate_user(user_id)
    if success:
        return jsonify({"success": True, "message": "User activated successfully"}), 200

    return jsonify({"success": False, "message": "Failed to activate user"}), 400
