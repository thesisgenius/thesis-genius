from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, g
from backend.app.services.userservice import UserService
from backend.app.utils.auth import jwt_required

user_bp = Blueprint("user_api", __name__, url_prefix="/api/v1/user",
                    template_folder="templates",
                    static_folder="static",)

# Instantiate UserService
user_service = UserService()

@user_bp.route("/profile", methods=["GET"])
@jwt_required
def user_profile():
    """
    Fetch the authenticated user's profile data.
    """
    user_id = g.user_id  # Get the user ID from the middleware
    user_data = user_service.get_user_data(user_id)
    if not user_data:
        flash("User not found", "error")
        return redirect(url_for("auth.login"))  # Redirect to login page if user not found
    return render_template("user/profile.html", user=user_data)


@user_bp.route("/profile/edit", methods=["GET", "POST"])
@jwt_required
def edit_profile():
    """
    Fetch and update the authenticated user's profile data.
    """
    user_id = g.user_id
    if request.method == "POST":
        update_data = {
            "name": request.form["name"],
            "email": request.form["email"],
        }
        success = user_service.update_user_data(user_id, update_data)
        if success:
            flash("Profile updated successfully!", "success")
            return redirect(url_for(".user_profile"))
        flash("Failed to update profile.", "error")
    user_data = user_service.get_user_data(user_id)
    return render_template("user/edit_profile.html", user=user_data)


@user_bp.route("/profile", methods=["PUT"])
@jwt_required
def update_profile():
    """
    Update the authenticated user's profile data (API endpoint).
    """
    user_id = g.user_id
    update_data = request.json
    success = user_service.update_user_data(user_id, update_data)
    if success:
        return jsonify({"message": "Profile updated successfully."}), 200
    return jsonify({"error": "Failed to update profile."}), 400
