from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.thesisservice import ThesisService
from ..utils.auth import jwt_required

thesis_bp = Blueprint("thesis_api", __name__, url_prefix="/api/thesis")


@thesis_bp.route("/theses", methods=["GET"])
@jwt_required
def list_theses():
    """
    Fetch all theses created by the authenticated user.
    """
    # Instantiate ThesisService
    thesis_service = ThesisService(app.logger)
    user_id = g.user_id
    try:
        theses = thesis_service.get_user_theses(user_id)
        return jsonify({"success": True, "theses": theses}), 200
    except Exception as e:
        app.logger.error(f"Error fetching theses for user {user_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch theses"}), 500


@thesis_bp.route("/thesis", methods=["POST"])
@jwt_required
def create_thesis():
    """
    Create a new thesis.
    """
    # Instantiate ThesisService
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        title = data.get("title")
        abstract = data.get("abstract")
        status = data.get("status")

        if not title or not abstract or not status:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title, abstract, and status are required",
                    }
                ),
                400,
            )

        user_id = g.user_id
        success = thesis_service.create_thesis(
            user_id, {"title": title, "abstract": abstract, "status": status}
        )
        if success:
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"{title.capitalize()} Thesis created successfully",
                        "id": success["id"],
                    }
                ),
                201,
            )
        return jsonify({"success": False, "message": "Failed to create thesis"}), 400
    except Exception as e:
        app.logger.error(f"Error creating thesis: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/thesis/<int:thesis_id>", methods=["PUT"])
@jwt_required
def edit_thesis(thesis_id):
    """
    Update an existing thesis.
    """
    # Instantiate ThesisService
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "Invalid payload"}), 400

        updated_data = {
            "title": data.get("title"),
            "abstract": data.get("abstract"),
            "status": data.get("status"),
        }

        if (
            not updated_data["title"]
            or not updated_data["abstract"]
            or not updated_data["status"]
        ):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title, abstract, and status are required",
                    }
                ),
                400,
            )

        success = thesis_service.update_thesis(thesis_id, user_id, updated_data)
        if success:
            return (
                jsonify({"success": True, "message": "Thesis updated successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to update thesis"}), 400
    except Exception as e:
        app.logger.error(f"Error updating thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/thesis/<int:thesis_id>", methods=["DELETE"])
@jwt_required
def delete_thesis(thesis_id):
    """
    Delete an existing thesis.
    """
    # Instantiate ThesisService
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        success = thesis_service.delete_thesis(thesis_id, user_id)
        if success:
            return (
                jsonify({"success": True, "message": "Thesis deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete thesis"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500
