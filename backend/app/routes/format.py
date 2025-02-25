# format.py
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, make_response, request, send_file

from ..services.apaservice import APAService
from ..utils.auth import jwt_required
from ..utils.formatter import APAFormatter

format_bp = Blueprint("format_bp", __name__, url_prefix="/api/format")


@format_bp.route("/apa/<int:thesis_id>", methods=["GET"])
@jwt_required
def get_apa_format(thesis_id):
    """
    Return the thesis data in different formats:
      - ?format=json => returns aggregator JSON
      - ?format=html => returns APA-style HTML
      - ?format=docx => returns a Word file
      - ?format=pdf  => returns a PDF
    """
    apa_service = APAService(app.logger)
    output = request.args.get("format", "json")
    try:
        data = apa_service.get_thesis_data(thesis_id)

        if not data:
            return jsonify({"error": "Thesis not found"}), 404

        title = data.get("cover").get("title")

        if output == "json":
            return jsonify(data), 200

        elif output == "html":
            html_str = APAFormatter.to_html(data)
            return make_response(html_str, 200)

        elif output == "docx":
            doc_stream = APAFormatter.to_docx(data)
            # Return as a file download
            # We'll guess a filename, e.g. "thesis.docx"
            return send_file(
                doc_stream,
                as_attachment=True,
                download_name=f"{title}.docx",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        elif output == "pdf":
            pdf_stream = APAFormatter.to_pdf(data)
            return send_file(
                pdf_stream,
                as_attachment=True,
                download_name="thesis.pdf",
                mimetype="application/pdf",
            )

        else:
            app.logger.error(f"Unsupported format: {output}")
            return jsonify({"error": "Unsupported format"}), 400

    except ValueError as e:
        app.logger.error(f"ValueError during thesis format conversion: {e}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        app.logger.error(f"Exception error during thesis format conversion: {e}")
        return jsonify({"error": str(e)}), 500
