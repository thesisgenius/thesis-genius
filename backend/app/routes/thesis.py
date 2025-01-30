from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request
from playhouse.shortcuts import model_to_dict

from ..models.data import Thesis
from ..services.thesisservice import ThesisService
from ..utils.auth import jwt_required

thesis_bp = Blueprint("thesis_api", __name__, url_prefix="/api/thesis")


@thesis_bp.route("/theses", methods=["GET"])
@jwt_required
def list_theses():
    """
    Fetch all theses created by the authenticated user.
    """

    thesis_service = ThesisService(app.logger)
    user_id = g.user_id
    try:
        theses = thesis_service.get_user_theses(user_id)
        return jsonify({"success": True, "theses": theses}), 200
    except Exception as e:
        app.logger.error(f"Error fetching theses for user {user_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch theses"}), 500


@thesis_bp.route("/<int:thesis_id>", methods=["GET"])
@jwt_required
def get_thesis(thesis_id):
    """
    Fetch a single thesis by its ID.
    """
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        thesis = thesis_service.get_thesis_by_id(thesis_id, user_id)

        if thesis:
            thesis_dict = model_to_dict(
                thesis, exclude=[Thesis.student]
            )  # Exclude the student object
            thesis_dict["student_id"] = thesis.student_id  # Add student_id explicitly
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Thesis fetched successfully",
                        "thesis": thesis_dict,
                    }
                ),
                200,
            )

        return (
            jsonify(
                {"success": False, "message": "Thesis not found or not accessible."}
            ),
            404,
        )
    except Exception as e:
        app.logger.error(f"Error fetching thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/new", methods=["POST"])
@jwt_required
def create_thesis():
    """
    Create a new thesis.
    """
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        if not data:
            return (
                jsonify({"success": False, "message": "Request body is required"}),
                400,
            )

        title = data.get("title")
        abstract = data.get("abstract")
        content = data.get("content")
        status = data.get("status")

        if not title or not status:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title and status are required",
                    }
                ),
                400,
            )

        user_id = g.user_id
        if not user_id:
            return jsonify({"success": False, "message": "User ID is missing"}), 400

        thesis_data = {
            "title": title,
            "abstract": abstract,
            "content": content,
            "status": status,
            "student_id": user_id,  # Updated to conform to schema
        }
        thesis = thesis_service.create_thesis(thesis_data)

        if thesis:
            thesis_dict = model_to_dict(
                thesis, exclude=[Thesis.student]
            )  # Exclude student object
            thesis_dict["student_id"] = thesis.student_id  # Add student_id explicitly
            return (
                jsonify(
                    {
                        "success": True,
                        "message": f"Thesis '{title}' created successfully",
                        "thesis": thesis_dict,
                        "id": thesis.id,
                    }
                ),
                201,
            )

        return jsonify({"success": False, "message": "Failed to create thesis"}), 400
    except Exception as e:
        app.logger.error(f"Error creating thesis: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>", methods=["PUT"])
@jwt_required
def edit_thesis(thesis_id):
    """
    Update an existing thesis.
    """
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        data = request.json
        if not data:
            return (
                jsonify({"success": False, "message": "Request body is required"}),
                400,
            )

        updated_data = {}
        if data.get("title"):
            updated_data["title"] = data.get("title")
        if data.get("abstract"):
            updated_data["abstract"] = data.get("abstract")
        if data.get("status"):
            updated_data["status"] = data.get("status")
        if data.get("content"):
            updated_data["content"] = data.get("content")

        if not all(updated_data.values()):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title, abstract, and status are required",
                    }
                ),
                400,
            )
        # Log the incoming data
        app.logger.debug(
            f"Updating thesis {thesis_id} for user {user_id} with data: {updated_data}"
        )

        thesis = thesis_service.update_thesis(thesis_id, user_id, updated_data)
        if thesis:
            thesis_dict = model_to_dict(
                thesis, exclude=[Thesis.student]
            )  # Exclude student object
            return (
                jsonify(
                    {
                        "success": True,
                        "message": "Thesis updated successfully",
                        "thesis": thesis_dict,
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "success": False,
                    "message": "Failed to update thesis. Check if it exists and belongs to you.",
                }
            ),
            400,
        )
    except Exception as e:
        app.logger.error(f"Error updating thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>", methods=["DELETE"])
@jwt_required
def delete_thesis(thesis_id):
    """
    Delete an existing thesis.
    """

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


# --- References Endpoints ---
@thesis_bp.route("/<int:thesis_id>/references", methods=["POST"])
@jwt_required
def add_reference(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        reference = thesis_service.add_reference(thesis_id, data)
        return jsonify({"success": True, "reference": model_to_dict(reference)}), 201
    except Exception as e:
        app.logger.error(f"Error adding reference: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/<int:thesis_id>/references", methods=["GET"])
@jwt_required
def list_references(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        references = thesis_service.get_references(thesis_id)
        return jsonify({"success": True, "references": references}), 200
    except Exception as e:
        app.logger.error(f"Error fetching references: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/reference/<int:reference_id>", methods=["PUT"])
@jwt_required
def update_reference(reference_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_reference = thesis_service.update_reference(reference_id, data)
        return (
            jsonify({"success": True, "reference": model_to_dict(updated_reference)}),
            200,
        )
    except Exception as e:
        app.logger.error(f"Error updating reference: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/reference/<int:reference_id>", methods=["DELETE"])
@jwt_required
def delete_reference(reference_id):

    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_reference(reference_id)
        if success:
            return (
                jsonify({"success": True, "message": "Reference deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete reference"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting reference: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


# --- Footnotes Endpoints ---
@thesis_bp.route("/<int:thesis_id>/footnotes", methods=["POST"])
@jwt_required
def add_footnote(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        footnote = thesis_service.add_footnote(thesis_id, data)
        return jsonify({"success": True, "footnote": model_to_dict(footnote)}), 201
    except Exception as e:
        app.logger.error(f"Error adding footnote: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/<int:thesis_id>/footnotes", methods=["GET"])
@jwt_required
def list_footnotes(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        footnotes = thesis_service.get_footnotes(thesis_id)
        return jsonify({"success": True, "footnotes": footnotes}), 200
    except Exception as e:
        app.logger.error(f"Error fetching footnotes: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/footnote/<int:footnote_id>", methods=["PUT"])
@jwt_required
def update_footnote(footnote_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_footnote = thesis_service.update_footnote(footnote_id, data)
        return (
            jsonify({"success": True, "footnote": model_to_dict(updated_footnote)}),
            200,
        )
    except Exception as e:
        app.logger.error(f"Error updating footnote: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/footnote/<int:footnote_id>", methods=["DELETE"])
@jwt_required
def delete_footnote(footnote_id):

    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_footnote(footnote_id)
        if success:
            return (
                jsonify({"success": True, "message": "Footnote deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete footnote"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting footnote: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


# --- Tables Endpoints ---
@thesis_bp.route("/<int:thesis_id>/tables", methods=["POST"])
@jwt_required
def add_table(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        table = thesis_service.add_table(thesis_id, data)
        return jsonify({"success": True, "table": model_to_dict(table)}), 201
    except Exception as e:
        app.logger.error(f"Error adding table: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/<int:thesis_id>/tables", methods=["GET"])
@jwt_required
def list_tables(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        tables = thesis_service.get_tables(thesis_id)
        return jsonify({"success": True, "tables": tables}), 200
    except Exception as e:
        app.logger.error(f"Error fetching tables: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/table/<int:table_id>", methods=["PUT"])
@jwt_required
def update_table(table_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_table = thesis_service.update_table(table_id, data)
        return jsonify({"success": True, "table": model_to_dict(updated_table)}), 200
    except Exception as e:
        app.logger.error(f"Error updating table: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/table/<int:table_id>", methods=["DELETE"])
@jwt_required
def delete_table(table_id):

    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_table(table_id)
        if success:
            return (
                jsonify({"success": True, "message": "Table deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete table"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting table: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


# --- Figures Endpoints ---
@thesis_bp.route("/<int:thesis_id>/figures", methods=["POST"])
@jwt_required
def add_figure(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        figure = thesis_service.add_figure(thesis_id, data)
        return jsonify({"success": True, "figure": model_to_dict(figure)}), 201
    except Exception as e:
        app.logger.error(f"Error adding figure: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/<int:thesis_id>/figures", methods=["GET"])
@jwt_required
def list_figures(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        figures = thesis_service.get_figures(thesis_id)
        return jsonify({"success": True, "figures": figures}), 200
    except Exception as e:
        app.logger.error(f"Error fetching figures: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/figure/<int:figure_id>", methods=["PUT"])
@jwt_required
def update_figure(figure_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_figure = thesis_service.update_figure(figure_id, data)
        return jsonify({"success": True, "figure": model_to_dict(updated_figure)}), 200
    except Exception as e:
        app.logger.error(f"Error updating figure: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/figure/<int:figure_id>", methods=["DELETE"])
@jwt_required
def delete_figure(figure_id):

    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_figure(figure_id)
        if success:
            return (
                jsonify({"success": True, "message": "Figure deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete figure"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting figure: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


# --- Appendices Endpoints ---
@thesis_bp.route("/<int:thesis_id>/appendices", methods=["POST"])
@jwt_required
def add_appendix(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        appendix = thesis_service.add_appendix(thesis_id, data)
        return jsonify({"success": True, "appendix": model_to_dict(appendix)}), 201
    except Exception as e:
        app.logger.error(f"Error adding appendix: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/<int:thesis_id>/appendices", methods=["GET"])
@jwt_required
def list_appendices(thesis_id):

    thesis_service = ThesisService(app.logger)
    try:
        appendices = thesis_service.get_appendices(thesis_id)
        return jsonify({"success": True, "appendices": appendices}), 200
    except Exception as e:
        app.logger.error(f"Error fetching appendices: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/appendix/<int:appendix_id>", methods=["PUT"])
@jwt_required
def update_appendix(appendix_id):

    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_appendix = thesis_service.update_appendix(appendix_id, data)
        return (
            jsonify({"success": True, "appendix": model_to_dict(updated_appendix)}),
            200,
        )
    except Exception as e:
        app.logger.error(f"Error updating appendix: {e}")
        return jsonify({"success": False, "message": str(e)}), 400


@thesis_bp.route("/appendix/<int:appendix_id>", methods=["DELETE"])
@jwt_required
def delete_appendix(appendix_id):

    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_appendix(appendix_id)
        if success:
            return (
                jsonify({"success": True, "message": "Appendix deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete appendix"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting appendix: {e}")
        return jsonify({"success": False, "message": str(e)}), 400
