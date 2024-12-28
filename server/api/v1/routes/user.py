# api/v1/routes/user.py
from flask import Blueprint, jsonify, request

from server.models.user import User
from server.utils.auth import token_required

user_bp_v1 = Blueprint("user_v1", __name__, url_prefix="/users")


@user_bp_v1.route("/register", methods=["POST"])
def register_user():
    data = request.json

    # Validate required fields
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing email or password"}), 400

    # Call User.register() method
    user = User.register(data)
    if user:
        return jsonify({"id": user.id, "message": "User registered successfully"}), 201
    return jsonify({"error": "User registration failed"}), 400


@user_bp_v1.route("/login", methods=["POST"])
def login_user():
    data = request.json
    token = User.login(data["email"], data["password"])
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@user_bp_v1.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    return (
        jsonify(
            {
                "id": current_user.id,
                "email": current_user.email,
                "created_at": current_user.created_at,
            }
        ),
        200,
    )
