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
    Retrieves a list of theses associated with the authenticated user.

    This function handles the HTTP GET request to retrieve theses linked to the
    currently authenticated user. It utilizes a ThesisService instance to fetch
    user-specific theses and returns them in a JSON response. If an exception
    occurs, an error is logged, and a failure response is returned.

    :raises Exception: If there is an error fetching theses for the user.

    :return: A tuple containing a JSON response with either a list of theses or
        an error message, along with the appropriate HTTP status code.
    :rtype: tuple
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
    Fetches a specific thesis by its ID for the authenticated user.

    This endpoint allows users to retrieve details of a thesis identified by the given
    thesis ID. The endpoint requires the user to be authenticated via a JWT, and the
    thesis must be accessible by the requesting user. If the thesis exists and is accessible,
    the details are returned in the response; otherwise, an appropriate error message
    is provided.

    :param thesis_id: The unique identifier of the thesis to fetch.
    :type thesis_id: int
    :return: A JSON object with details of the thesis if found, or an error message
        indicating either the thesis is not found, not accessible, or
        an internal server error occurred.
    :rtype: Tuple[Response, int]
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

@thesis_bp.route("/<int:thesis_id>/cover-page", methods=["GET"])
@jwt_required
def get_cover_page(thesis_id):
    """
    Retrieves the cover page details for a specific thesis.
    """
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        cover_page = thesis_service.get_cover_page(thesis_id, user_id)

        if cover_page:
            return jsonify({"success": True, "cover_page": cover_page}), 200
        return jsonify({"success": False, "message": "Cover page not found"}), 404

    except Exception as e:
        app.logger.error(f"Error fetching cover page for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>/cover-page", methods=["PUT"])
@jwt_required
def update_cover_page(thesis_id):
    """
    Updates the cover page details for a specific thesis.

    :param thesis_id: The ID of the thesis whose cover page is being updated.
    :type thesis_id: int
    :return: A JSON response indicating the success or failure of the update.
    """
    thesis_service = ThesisService(app.logger)
    try:
        user_id = g.user_id
        data = request.json

        updated_cover_page = thesis_service.update_cover_page(thesis_id, user_id, dict(data))

        if updated_cover_page:
            return jsonify({"success": True, "cover_page": updated_cover_page}), 200
        return jsonify({"success": False, "message": "Failed to update cover page"}), 400

    except Exception as e:
        app.logger.error(f"Error updating cover page for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500

@thesis_bp.route("/<int:thesis_id>/table-of-contents", methods=["GET"])
@jwt_required
def get_toc(thesis_id):
    thesis_service = ThesisService(app.logger)
    try:
        toc = thesis_service.get_table_of_contents(thesis_id)
        return jsonify({"success": True, "table_of_contents": toc}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving TOC for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "Failed to retrieve TOC"}), 500


@thesis_bp.route("/<int:thesis_id>/table-of-contents", methods=["PUT"])
@jwt_required
def update_toc(thesis_id):
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json.get("table_of_contents", [])
        updated_toc = thesis_service.update_table_of_contents(thesis_id, data)
        return jsonify({"success": True, "table_of_contents": updated_toc}), 200
    except Exception as e:
        app.logger.error(f"Error updating TOC for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "Failed to update TOC"}), 500

@thesis_bp.route("/new", methods=["POST"])
@jwt_required
def create_thesis():
    """
    Handles the creation of a new thesis entry by the authenticated user. The function validates
    input data provided in the request, ensures required fields are populated, and interacts
    with the ThesisService to persist the data in the database. If the creation is successful,
    returns a JSON response including the newly created thesis details; otherwise, returns
    appropriate error responses.

    :param request.json: JSON-encoded request data containing the thesis details to be created.
        It may include the following keys: "title" (required, string), "abstract" (optional, string),
        "content" (optional, string), and "status" (required, string).
    :return: A Flask JSON response object.
        On success: Response with HTTP 201 status containing thesis details and a success message.
        On failure: Response with HTTP 400 status and an error message for invalid/missing data.
        On internal server error: Response with HTTP 500 status and a generic error message.

    :raises:
        - If the request JSON is invalid or missing, raises an error with HTTP 400 response.
        - If "title" or "status" is not present in the request body, raises an error with HTTP 400 response.
        - If "user_id" is inaccessible from the global object, raises an error with HTTP 400 response.
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
            key: value
            for key, value in data.items()
            if key in ["title", "abstract", "status", "body_pages"]
        }
        thesis_data["student_id"] = user_id
        thesis = thesis_service.create_thesis(thesis_data)
        if not thesis:
            return (
                jsonify({"success": False, "message": "Failed to create thesis"}),
                400,
            )
        else:
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
    except Exception as e:
        app.logger.error(f"Error creating thesis: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>", methods=["PUT"])
@jwt_required
def edit_thesis(thesis_id):
    """
    Update an existing thesis based on the provided data and thesis ID. The user must
    be authenticated to perform this operation. The function retrieves the user ID
    from the JWT token, validates the request body, and updates the thesis data
    using the service layer. It ensures that all required fields are provided
    before proceeding with the update.

    :param thesis_id: The ID of the thesis to be updated.
    :type thesis_id: int
    :raises ValueError: If the request body is missing or mandatory fields are not provided.
    :return: JSON response indicating success or failure, along with the updated thesis
        data if the update is successful.
    :rtype: flask.Response
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

        updated_data = {
            key: value
            for key, value in dict(data).items()
            if key in ["title", "status"]
        }

        if not all(updated_data.values()):
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Title and status are required",
                    }
                ),
                400,
            )
        # Log the incoming data
        app.logger.debug(
            f"Updating thesis {thesis_id} for user {user_id} with data: {updated_data}"
        )

        thesis = thesis_service.update_thesis(thesis_id, user_id, updated_data)
        if not thesis:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Failed to update thesis. Check if it exists and belongs to you.",
                    }
                ),
                400,
            )

        # Handle abstract updates
        if "abstract" in data:
            thesis_service.add_abstract(thesis.id, data["abstract"])

        # Handle body pages updates
        if "body_pages" in data:
            for page in data["body_pages"]:
                thesis_service.add_body_page(
                    thesis.id, page["page_number"], page["body"]
                )

        thesis_dict = model_to_dict(thesis, exclude=[thesis.student])
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

    except Exception as e:
        app.logger.error(f"Error updating thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>", methods=["DELETE"])
@jwt_required
def delete_thesis(thesis_id):
    """
    Deletes a thesis record associated with the provided thesis ID and
    user ID.

    This endpoint deletes a specific thesis identified by its ID, if the
    user has the permission to delete it. It logs the result of the operation
    and provides appropriate HTTP status codes for success and error
    responses.

    :param thesis_id: The ID of the thesis to be deleted, passed as part
                      of the route.
    :type thesis_id: int
    :return: A JSON response containing the operation result and a corresponding
             HTTP status code.
    :rtype: Tuple[Response, int]
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


# ----------------- ABSTRACT ROUTES -----------------
@thesis_bp.route("/<int:thesis_id>/abstract", methods=["GET"])
@jwt_required
def get_abstract(thesis_id):
    """
    Retrieves the abstract for a specific thesis identified by the provided ID.

    This endpoint allows a user to fetch the abstract of a particular thesis.
    It requires authentication via JWT. On success, it returns the abstract
    text for the thesis.

    :param thesis_id: The ID of the thesis whose abstract is to be retrieved.
    :type thesis_id: int
    :return: JSON response containing the abstract text and success status, or an
             error message if the operation fails.
    :rtype: tuple (dict, int)
    """
    thesis_service = ThesisService(app.logger)
    try:
        abstract_text = thesis_service.get_abstract(thesis_id)
        return jsonify({"success": True, "abstract": abstract_text}), 200
    except ValueError as e:
        # This exception is raised when no abstract is found for the thesis ID
        app.logger.info(str(e))
        return jsonify({"success": False, "message": str(e)}), 404
    except Exception as e:
        # Any other unexpected errors
        app.logger.error(f"Error retrieving abstract for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500



@thesis_bp.route("/<int:thesis_id>/abstract", methods=["POST"])
@jwt_required
def create_or_update_abstract(thesis_id):
    """
    Creates or updates an abstract for a thesis with the provided `thesis_id`.
    The function handles POST requests, retrieves the abstract text from the
    incoming JSON payload, and attempts to either create or update the abstract
    associated with the specified `thesis_id`. If an error occurs during processing,
    an error response is returned, and the corresponding error is logged.

    :param thesis_id: The unique identifier for the thesis whose abstract is being
        created or updated.
    :type thesis_id: int
    :return: A JSON response with the success status and message indicating the
        result of the operation. Possible HTTP status codes: 200 (success),
        400 (failure to update abstract), or 500 (internal error).
    :rtype: flask.Response
    """
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        abstract_text = data.get("text", "")
        abstract = thesis_service.add_abstract(thesis_id, abstract_text)
        if abstract:
            return jsonify({"success": True, "message": "Abstract updated"}), 200
        return jsonify({"success": False, "message": "Failed to update abstract"}), 400

    except Exception as e:
        app.logger.error(f"Error updating abstract for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@thesis_bp.route("/<int:thesis_id>/abstract", methods=["DELETE"])
@jwt_required
def delete_abstract(thesis_id):
    """
    Deletes the abstract of a thesis identified by its ID.

    This endpoint allows a user to delete an existing abstract for a specific
    thesis by providing the thesis ID. The operation requires authentication
    via JWT. Upon successful deletion, a success message is returned.

    :param thesis_id: The ID of the thesis whose abstract is to be deleted
    :type thesis_id: int
    :return: JSON response confirming the success of the operation and an
        associated message
    :rtype: tuple (dict, int)
    """
    thesis_service = ThesisService(app.logger)
    try:
        thesis_service.delete_abstract(thesis_id)
    except Exception as e:
        app.logger.error(f"Error deleting abstract for thesis {thesis_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500
    return jsonify({"success": True, "message": "Abstract deleted"}), 200


# ----------------- BODY PAGE ROUTES -----------------
@thesis_bp.route("/<int:thesis_id>/body-pages", methods=["GET"])
@jwt_required
def get_body_pages(thesis_id):
    """
    Retrieve all body pages for a specific thesis identified by its ID.
    This function fetches the body pages using ThesisService and returns
    the data in JSON format.

    :param thesis_id: The ID of the thesis whose body pages are to be retrieved.
    :type thesis_id: int
    :return: A JSON response containing success status and a list of body pages if successful,
             or failure status and a message if unsuccessful.
    :rtype: flask.Response
    """
    thesis_service = ThesisService(app.logger)
    try:
        # Call the service method to fetch the body pages
        body_pages = thesis_service.get_body_pages(thesis_id)

        if body_pages:
            return jsonify(
                {
                    "success": True,
                    "message": f"Successfully retrieved body pages for thesis ID {thesis_id}",
                    "body_pages": body_pages,
                }
            ), 200
        else:
            return jsonify({"success": False, "message": "No body pages found"}), 404
    except Exception as e:
        app.logger.error(f"Error retrieving body pages for thesis ID {thesis_id}: {e}")
        return jsonify({"success": False, "message": "Failed to retrieve body pages"}), 500



@thesis_bp.route("/<int:thesis_id>/body-pages", methods=["POST"])
@jwt_required
def add_body_page(thesis_id):
    """
    Add a new body page to an existing thesis. This function allows adding a body page
    to a specific thesis identified by its ID. It extracts the page number and body content
    from the request JSON payload and creates a new body page using the ThesisService.
    The response includes a success or failure message along with the newly created
    page's ID if successful.

    :param thesis_id: The ID of the thesis to which the body page is to be added
    :type thesis_id: int
    :return: A JSON response with success status, message, and page ID if successful,
        or failure status and message if not.
    :rtype: flask.Response
    """
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        page = thesis_service.add_body_page(
            thesis_id, data.get("page_number"), data.get("body")
        )
        if page:
            return (
                jsonify(
                    {"success": True, "message": "Body page added", "page_id": page.id}
                ),
                201,
            )
    except Exception as e:
        app.logger.error(f"Failed to add body page: {e}")
        return jsonify({"success": False, "message": "Failed to add body page"}), 400


@thesis_bp.route("/<int:thesis_id>/body-pages/<int:page_id>", methods=["PUT"])
@jwt_required
def update_body_page(thesis_id, page_id):
    """
    Updates a thesis body page with the provided details. It uses the ThesisService
    to update the page's content, given the page ID, page number, and body text.
    Returns a success response if the page is updated, otherwise a failure response.

    :param thesis_id:
    :param page_id: The ID of the page to be updated.
    :type page_id: int
    :return: A Flask JSON response indicating the success or failure of the operation.
    :rtype: flask.Response

    """
    thesis_service = ThesisService(app.logger)
    try:
        data = request.json
        updated_page = thesis_service.update_body_page(
            thesis_id, page_id, data["page_number"], data["body"]
        )
        if updated_page:
            return jsonify({"success": True, "message": "Body page updated"}), 200
    except Exception as e:
        app.logger.error(f"Error updating body page: {e}")
        return jsonify({"success": False, "message": "Failed to update body page"}), 400


@thesis_bp.route("/<int:thesis_id>/body-pages/<int:page_id>", methods=["DELETE"])
@jwt_required
def delete_body_page(thesis_id, page_id):

    """
    Deletes a body page from a thesis by its page ID. This function is protected
    by JWT authentication and interacts with the `ThesisService` to perform
    the deletion. After successful deletion, it returns a success response
    with a message indicating that the body page has been deleted.

    :param page_id: The ID of the page to be deleted.
    :type page_id: int
    :return: A dictionary containing success status and deletion message,
             along with HTTP status code 200.
    :rtype: tuple
    """
    thesis_service = ThesisService(app.logger)
    try:
        success = thesis_service.delete_body_page(thesis_id, page_id)
        if success:
            return jsonify({"success": True, "message": "Body page deleted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Failed to delete body page: {e}")
        return jsonify({"success": False, "message": "Failed to delete body page"}), 400


# --- References Endpoints ---
@thesis_bp.route("/<int:thesis_id>/references", methods=["POST"])
@jwt_required
def add_reference(thesis_id):
    """
    Handles the HTTP POST request to add a reference to a thesis. This endpoint
    requires authentication via JWT. A JSON payload containing reference details
    is expected in the request body. Upon successful addition of the reference,
    a JSON response containing the new reference details is returned with HTTP
    status 201. If an error occurs, an error message is logged and a JSON response
    with the error details is returned with HTTP status 400.

    :param thesis_id: The unique identifier of the thesis to which the reference
                      should be added
    :type thesis_id: int
    :return: A JSON response indicating success or failure. If successful, includes
             details of the added reference.
    :rtype: tuple (dict, int)
    """
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
    """
    Fetch the list of references associated with a specific thesis.

    This endpoint is responsible for retrieving all references tied to a given
    thesis ID. It requires authentication via a JWT token. The function
    utilizes the ThesisService to handle the business logic for fetching
    references. Success or failure responses are returned in JSON format.

    :param thesis_id: An integer indicating the unique identifier of the thesis.
    :return: On success, returns a JSON object containing a success flag and
        the list of references (HTTP status code 200). On failure,
        returns a JSON object with a success flag set to False and the
        error message (HTTP status code 400).
    """
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
    """
    Updates a reference entry identified by its ID with new data. This function
    is intended to be used with the PUT HTTP method and requires authentication
    using JWT. It integrates with the `ThesisService` class to handle the
    update operation and logs errors if the update fails.

    :param reference_id: The ID of the reference to be updated.
    :type reference_id: int
    :return: A JSON response with the success status and updated reference
        details if the operation is successful, or an error message if it fails.
    :rtype: tuple
    """
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
    """
    Handles the deletion of a reference with the given ID. This endpoint is protected
    by a JWT and allows only authenticated users to delete references. The method interacts
    with the ThesisService to perform the deletion operation, logs any errors, and returns
    an appropriate JSON response with a success or failure message.

    :param reference_id: The integer ID of the reference to be deleted.
    :type reference_id: int
    :return: A JSON response indicating whether the reference was deleted successfully,
             along with the appropriate HTTP status code.
    :rtype: Tuple of a dictionary and an integer
    """
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
    """
    Add a new footnote to a specific thesis by its ID. This endpoint is protected
    and requires a valid JWT token for access. The provided footnote details in the
    request body will be used to create the footnote. Sends back a JSON response
    on success or failure.

    :param thesis_id: The ID of the thesis to which the footnote is to be added.
    :type thesis_id: int
    :return: A JSON response containing the success state and details of the
             newly added footnote or an error message.
    :rtype: Response
    """
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
    """
    Fetches and returns the list of footnotes associated with a specific thesis.

    This function handles HTTP GET requests to retrieve a list of footnotes for a
    given thesis based on its ID. It utilizes the ``ThesisService`` to perform the
    operation and logs errors if the retrieval operation fails. The response will
    contain the list of footnotes if successful or an error message if the operation
    encounters an exception.

    :param thesis_id: The unique identifier of the thesis whose footnotes are to be
        retrieved.
    :type thesis_id: int
    :return: A JSON response containing success status along with the list of
        footnotes if the operation is successful, otherwise an error message.
    :rtype: Tuple[Response, int]
    """
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
    """
    Updates an existing footnote with provided data.

    This endpoint allows updating the details of an existing footnote identified
    by its footnote ID. The updated footnote data is provided in the request
    payload and processed by the `ThesisService` to perform the update operation.
    Upon successful update, a JSON response containing the updated footnote data
    is returned.

    :param footnote_id: Identifier of the footnote to be updated.
    :type footnote_id: int
    :return: A JSON response containing the status of the update operation and
        the updated footnote data, if the update is successful. In case of a
        failure, a JSON response with an error message is returned.
    :rtype: Tuple[flask.Response, int]
    """
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
    """
    Deletes a footnote with the given ID.

    This method allows the deletion of a specific footnote by
    providing its ID. It communicates with the `ThesisService`
    to attempt removal of the specified footnote and returns a
    JSON response indicating the success or failure of the
    operation. If an exception occurs during the process, an
    error response is returned, and the exception is logged.

    :param footnote_id: The ID of the footnote to be deleted.
    :type footnote_id: int
    :return: A JSON response indicating success or failure of the operation.
    :rtype: Response
    """
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
    """
    This function is an endpoint to add a new table to a specific thesis. It uses the provided
    ``thesis_id`` and the table data from the request JSON payload, processes it through the thesis
    service, and returns the newly added table in JSON format if successful. In case of a failure,
    it logs the error and sends an error message in the response.

    :param thesis_id: The unique identifier for the thesis to which the table is being added.
    :type thesis_id: int

    :return: A JSON response containing a success status and the newly added table if the
        operation is successful, or an error message otherwise.
    :rtype: tuple
    """
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
    """
    Fetches and returns the tables associated with a specific thesis.

    This function handles the retrieval of tables linked to a given thesis ID.
    It leverages the ThesisService class to perform the database operations
    and returns the results in JSON format with appropriate HTTP status codes.
    If an error occurs, it logs the error and provides an error message in the
    response.

    :param thesis_id: The ID of the thesis for which tables are being fetched.
    :type thesis_id: int
    :return: A JSON response containing a success indicator and a list of tables
        if successful, or an error message if an exception occurs.
    :rtype: flask.Response
    """
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
    """
    Updates a table in the thesis management system with the provided data.

    This function is an endpoint that processes a PUT request to update an
    existing table identified by its ID. It invokes the `update_table` method
    from the `ThesisService` class, passing the table ID and the JSON payload
    received in the request. The response includes the updated table data in
    JSON format if the operation is successful, or an error message otherwise.

    :param table_id: The ID of the table to be updated
    :type table_id: int
    :return: A JSON response containing either the updated table data or an
        error message. On success, the response includes a `success` flag set
        to `True`, and the updated table object serialized into a dictionary
        format. On failure, the response includes a `success` flag set to
        `False` and an error message.
    :rtype: tuple(dict, int)
    """
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
    """
    Deletes a table identified by its unique ID. This function handles the HTTP DELETE
    request method and is responsible for invoking the `ThesisService` to perform the
    deletion operation. If the deletion is successful, a corresponding success message
    is returned; otherwise, an error message is returned. The function also logs any
    exceptions during the process.

    :param table_id: Unique identifier of the table to be deleted
    :type table_id: int
    :return: A JSON response indicating success or failure message with appropriate
        HTTP status codes. On success, returns HTTP 200; on failure, returns HTTP 400
    :rtype: Tuple[flask.Response, int]
    """
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
    """
    Adds a new figure to a thesis by its ID.

    This endpoint allows users to add a figure to a specified thesis, identified by its
    unique thesis ID. The figure data must be provided in the request body as JSON. A successful
    operation will return the newly created figure in JSON format.

    :param thesis_id: The unique identifier of the thesis to which the figure will be added.
    :type thesis_id: int
    :return: A JSON response containing the success status and the newly created figure data.
    :rtype: Tuple[dict, int]
    """
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
    """
    Fetches the figures associated with a given thesis ID. This endpoint is
    protected and requires a valid JWT token. The function interacts with
    the ThesisService to retrieve the list of figures for the specified
    thesis. If successful, the figures are returned in a JSON response.
    In case of errors during processing, an appropriate error message is
    logged and returned.

    :param thesis_id: The unique identifier of the thesis whose figures
                      are to be retrieved.
    :type thesis_id: int
    :return: A JSON response with a success status and a list of figures
             if the retrieval is successful, or an error message and
             failure status if an error occurs.
    :rtype: tuple
    """
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
    """
    Updates a specific figure by its ID with the provided new data. This endpoint
    is protected and requires a valid JWT for access. The updated figure details
    are returned in JSON format upon success.

    :param figure_id: The ID of the figure to be updated
    :type figure_id: int
    :return: JSON response containing the updated figure details and a success
             status in case of successful update, or an error message in case of
             failure
    :rtype: tuple
    """
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
    """
    Deletes a figure by its ID. This endpoint is protected and requires JWT
    authentication. It attempts to delete a figure using the `ThesisService`
    and returns a success or failure response.

    :param figure_id: The ID of the figure to be deleted.
    :type figure_id: int
    :return: A JSON response indicating success or failure along with
        appropriate HTTP status code.
    :rtype: tuple
    """
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
    """
    Adds an appendix to a thesis.

    This function allows adding an appendix to an existing thesis by processing
    the provided data. It takes the thesis ID as input, retrieves the JSON data
    from the request, and utilizes the thesis service to perform the addition.
    Upon success, it returns the added appendix data formatted as a dictionary.
    If any exception occurs during the operation, an error message is logged, and
    an appropriate response with error details is returned.

    :param thesis_id: An integer representing the ID of the thesis to which the
                      appendix will be added.
    :returns: A JSON response containing the success status, the added appendix
              data (if successful), or the error message in case of failure.
    :rtype: flask.Response
    """
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
    """
    Fetches and returns the list of appendices associated with a specific thesis.

    This function is a part of the thesis blueprint and handles GET requests to
    retrieve appendices related to a thesis identified by its unique `thesis_id`.
    It utilizes the `ThesisService` class to fetch the appendices. The response
    includes a JSON object indicating the success status and the list of appendices
    if successful, or an error message in case of failure.

    :param thesis_id: Unique identifier of the thesis for which appendices
        need to be fetched.
    :type thesis_id: int
    :return: A JSON object containing either the success status and the list of
        appendices or an error message in case of failure, along with an HTTP status
        code.
    :rtype: Tuple[dict, int]
    """
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
    """
    Updates an existing appendix identified by the provided appendix ID. The function
    uses the `ThesisService` to handle the update operation, which accepts the appendix
    ID and the new data to update the appendix. The updated appendix is then returned
    in JSON format. In case of an error, an appropriate error message is logged and
    returned.

    :param appendix_id: The unique identifier of the appendix to be updated.
    :type appendix_id: int
    :return: A JSON object containing the success status and the updated appendix
        details, or an error message in case of failure.
    :rtype: tuple (dict, int)
    """
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
    """
    Deletes an appendix with the specified `appendix_id`. This function is bound to the
    `DELETE` method of the `/appendix/<int:appendix_id>` route. It utilizes the service layer
    to perform the delete operation and logs any errors encountered during the operation.

    The function ensures proper response handling by returning appropriate HTTP status codes
    and messages indicating the success or failure of the operation.

    :param appendix_id: The unique identifier of the appendix to be deleted.
    :type appendix_id: int
    :return: A JSON response with `success` status and corresponding message. If the operation
        is successful, it returns a message stating "Appendix deleted successfully" with HTTP 200.
        Otherwise, it returns an error message with HTTP 400.
    :rtype: tuple
    """
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
