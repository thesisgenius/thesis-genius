from flask import Blueprint, jsonify, send_file

from ..services.apaservice import generate_apa_formatted_document

format_bp = Blueprint("format", __name__, url_prefix="/api/format")


@format_bp.route("/apa/<int:thesis_id>", methods=["GET"])
def format_to_apa_endpoint(thesis_id):
    """
    Generates and serves an APA-formatted document file for the given thesis ID.

    This endpoint retrieves a thesis identified by its ID, processes it to generate
    an APA-styled document, and sends the resulting file as a downloadable
    attachment. If the thesis is not found or an error occurs, an appropriate
    error response is returned.

    :param thesis_id: The unique identifier of the thesis to format.
    :type thesis_id: int
    :return: A file response containing the APA-formatted document on success,
        or a JSON error response in case of an error.
    :rtype: Response
    :raises ValueError: If the provided thesis ID is invalid or no corresponding
        thesis exists.
    :raises Exception: For any other unexpected errors occurring during processing.
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
