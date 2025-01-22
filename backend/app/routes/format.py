from flask import Blueprint, jsonify, send_file

from ..services.apaservice import generate_apa_formatted_document

format_bp = Blueprint("format", __name__, url_prefix="/api/format")


@format_bp.route("/apa/<int:thesis_id>", methods=["GET"])
def format_to_apa_endpoint(thesis_id):
    """
    API endpoint to generate APA-formatted thesis.
    :param thesis_id: ID of the thesis to format.
    """
    try:
        # Generate APA-formatted document
        apa_doc_path = generate_apa_formatted_document(thesis_id)

        # Return the document to the user

        return send_file(
            apa_doc_path, as_attachment=True, download_name="APA_Thesis.docx"
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
