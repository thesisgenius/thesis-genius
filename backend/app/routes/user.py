from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.userservice import UserService
from ..utils.auth import jwt_required

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
            "name": data.get("name"),
            "email": data.get("email"),
        }

        if not updated_data["name"] or not updated_data["email"]:
            return (
                jsonify({"success": False, "message": "Name and email are required"}),
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


@user_bp.route("/deactivate", methods=["POST"])
@jwt_required
def deactivate_user():
    """
    Deactivate the authenticated user's account.
    """
    # Instantiate UserService
    user_service = UserService(app.logger)
    try:
        user_id = g.user_id
        success = user_service.deactivate_user(user_id)
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