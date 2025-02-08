from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.forumservice import ForumService
from ..utils.auth import jwt_required

forum_bp = Blueprint("forum_api", __name__, url_prefix="/api/forum")


@forum_bp.route("/posts", methods=["GET"])
def list_posts():
    """
    Fetches and returns a list of forum posts based on the provided parameters. The user can control pagination
    and sorting of the posts through query parameters. Logs errors if fetching posts fails.

    :param page: The current page number for pagination. Default is 1.
    :type page: int
    :param per_page: The number of posts to include per page. Default is 10.
    :type per_page: int
    :param order_by: The field by which posts are ordered, including sort direction. Default is 'created_at.desc'.
    :type order_by: str

    :return: A JSON response containing forum posts and a status code. The response includes a 'success' field
             (True if posts are fetched successfully; False otherwise). On success, it also includes paginated
             post data.
    :rtype: tuple
    """
    forum_service = ForumService(app.logger)
    try:
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        order_by = request.args.get("order_by", default="created_at.desc")

        posts_data = forum_service.get_all_posts(
            page=page, per_page=per_page, order_by=order_by
        )
        return jsonify({"success": True, **posts_data}), 200
    except Exception as e:
        app.logger.error(f"Error fetching posts: {e}")
        return jsonify({"success": False, "message": "Failed to fetch posts"}), 500


@forum_bp.route("/posts/<int:post_id>", methods=["GET"])
def view_post(post_id):
    """
    Fetch and display the details of a specific forum post along with associated comments.

    This endpoint retrieves a forum post identified by its ID, alongside user details and
    paginated comments associated with the post.

    :param post_id: The unique identifier of the forum post to be retrieved.
    :type post_id: int
    :returns: A JSON response containing the post details, the user who created it, and
              paginated comments. If the post is not found, a 404 status code is returned
              with an error message. If an error occurs during processing, a 500 status
              code with a failure message is returned.
    :rtype: tuple
    """
    forum_service = ForumService(app.logger)
    try:
        # Fetch the post by ID
        post = forum_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"success": False, "message": "Post not found"}), 404

        # Pagination for comments
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        # Fetch comments for the post
        comments_data = forum_service.get_post_comments(
            post_id, page=page, per_page=per_page
        )

        # Format and return the response
        return (
            jsonify(
                {
                    "success": True,
                    "post": {
                        "id": post["id"],
                        "title": post["title"],
                        "description": post["description"],
                        "content": post["content"],
                        "created_at": post["created_at"],
                        "updated_at": post["updated_at"],
                    },
                    "user": {
                        "id": post["user_id"],  # User ID from the joined User table
                        "username": post["username"],
                        "first_name": post["first_name"],
                        "last_name": post["last_name"],
                    },
                    "comments": comments_data,
                }
            ),
            200,
        )
    except Exception as e:
        app.logger.error(f"Error fetching post {post_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch post"}), 500


@forum_bp.route("/posts/new", methods=["POST"])
@jwt_required
def create_post():
    """
    Handles the creation of a new forum post. This endpoint is protected by JWT
    authentication and requires the request to include a valid token. The function
    expects a JSON body with `title` and `content` fields. If the necessary data
    is provided, a new post will be created and a successful response will be
    sent back with the post's details. If any errors occur or validation fails,
    appropriate error messages and HTTP status codes will be returned.

    :param data: JSON request body containing the `title` and `content` of the post.
    :type data: dict

    :raises KeyError: If a required field is missing in the request data.

    :return: A JSON response indicating the success or failure of the post creation
             operation. On success, it includes details such as the user ID,
             post title, and generated post ID. On failure, an error message
             is included, potentially along with the HTTP status code.
    :rtype: tuple
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or "title" not in data or "content" not in data:
            return (
                jsonify(
                    {"success": False, "message": "Title and content are required"}
                ),
                400,
            )

        user_id = g.user_id
        post = forum_service.create_post(
            user_id, {"title": data["title"], "content": data["content"]}
        )
        if post:
            return (
                jsonify(
                    {
                        "success": True,
                        "post": data["title"],
                        "user": user_id,
                        "id": post["id"],
                    }
                ),
                201,
            )
        return jsonify({"success": False, "message": "Failed to create post"}), 400
    except Exception as e:
        app.logger.error(f"Error creating post: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required
def update_post(post_id):
    """
    Handles the PUT request for updating an existing forum post. Ensures the user is
    authenticated and authorized to update the post. Validates the provided data to confirm
    that at least one of the fields, `title` or `content`, is supplied for the update. If the
    post is successfully updated, a success message and status code are returned. Handles
    errors related to missing data, not found or unauthorized posts, as well as internal
    server errors.

    :param post_id: The ID of the forum post to be updated
    :type post_id: int
    :return: A Flask response object with a JSON payload indicating success or failure,
        and an appropriate HTTP status code
    :rtype: werkzeug.wrappers.response.Response
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or ("title" not in data and "content" not in data):
            return (
                jsonify({"success": False, "message": "Title or content is required"}),
                400,
            )

        user_id = g.user_id  # Ensure the user is authorized to update the post
        success = forum_service.update_post(post_id, data, user_id)
        if success:
            return (
                jsonify({"success": True, "message": "Post updated successfully"}),
                200,
            )
        return (
            jsonify({"success": False, "message": "Post not found or unauthorized"}),
            404,
        )
    except Exception as e:
        app.logger.error(f"Error updating post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required
def add_comment(post_id):
    """
    Adds a comment to a specific forum post using the provided post ID and
    content in the request payload.

    This function interacts with the forum service to handle comment creation
    for a given post. It requires the user to be authenticated and extracts
    the user ID from the user context (global `g` object). The function
    expects the request payload to contain the 'content' field.

    :param post_id: ID of the post to which the comment will be added
    :type post_id: int
    :return: A JSON response indicating success or failure of the operation.
    :rtype: flask.Response
    :raises: Exception - If an unknown error occurs during comment creation.
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or "content" not in data:
            return jsonify({"success": False, "message": "Content is required"}), 400

        user_id = g.user_id
        comment = forum_service.add_comment_to_post(
            user_id, post_id, {"content": data["content"]}
        )
        if comment:
            return jsonify({"success": True, "comment": comment["content"]}), 201
        return jsonify({"success": False, "message": "Failed to add comment"}), 400
    except Exception as e:
        app.logger.error(f"Error adding comment to post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required
def delete_post(post_id):
    """
    Deletes a forum post identified by a unique post ID. This endpoint is protected
    by JWT authentication, ensuring that only authorized users can perform this action.
    It verifies the logged-in user's permissions to delete the specified post and
    logs the operation. If the post cannot be found or the user is unauthorized,
    an appropriate HTTP status and message are returned. In case of an internal error,
    a 500 status code is returned.

    :param post_id: The unique identifier of the post to be deleted.
    :type post_id: int
    :return: A JSON response indicating success or failure of the delete operation,
        along with an appropriate HTTP status code.
    :rtype: tuple (flask.Response, int)
    """
    forum_service = ForumService(app.logger)
    try:
        user_id = g.user_id
        success = forum_service.delete_post(post_id, user_id)
        if success:
            return (
                jsonify({"success": True, "message": "Post deleted successfully"}),
                200,
            )
        return (
            jsonify({"success": False, "message": "Post not found or unauthorized"}),
            404,
        )
    except Exception as e:
        app.logger.error(f"Error deleting post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["GET"])
@jwt_required
def get_comment(post_id, comment_id):
    """
    Retrieves a specific comment based on the given post ID and comment ID. This
    endpoint is protected by JWT authentication. It uses the ForumService to
    fetch the comment and returns the result in JSON format. If the comment does
    not exist, or an error occurs during retrieval, appropriate error responses
    are returned.

    :param post_id: The ID of the post associated with the comment.
    :type post_id: int
    :param comment_id: The ID of the comment to retrieve.
    :type comment_id: int
    :return: JSON response including success status, comment data (if found),
        or error message.
    :rtype: flask.Response
    """
    forum_service = ForumService(app.logger)
    try:
        comment = forum_service.get_comment_by_id(post_id, comment_id)
        if comment:
            return jsonify({"success": True, "comment": comment}), 200
        return jsonify({"success": False, "message": "Comment not found"}), 404
    except Exception as e:
        app.logger.error(f"Error fetching comment {comment_id} for post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["PUT"])
@jwt_required
def update_comment(post_id, comment_id):
    """
    Updates the content of a specific comment associated with a specific post.

    Allows a user to update the content of a comment identified by its ID within a
    specific post. This function verifies the presence of the required data and
    attempts the update through the service layer. If successful, the comment content
    is updated; otherwise, an error response is provided.

    :param post_id: ID of the post the comment is associated with.
    :type post_id: int
    :param comment_id: ID of the comment to be updated.
    :type comment_id: int
    :return: JSON response indicating success or failure of the operation, along
             with the corresponding HTTP status code.
    :rtype: tuple
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or "content" not in data:
            return jsonify({"success": False, "message": "Content is required"}), 400

        success = forum_service.update_comment(post_id, comment_id, data["content"])
        if success:
            return (
                jsonify({"success": True, "message": "Comment updated successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to update comment"}), 400
    except Exception as e:
        app.logger.error(f"Error updating comment {comment_id} for post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required
def delete_comment(post_id, comment_id):
    """
    Deletes a comment from a specified post.

    This function is responsible for deleting a comment from a post using its identifiers.
    The user initiating the deletion must be authorized, as determined by their user ID.
    If successful, the comment will be removed; otherwise, it returns an appropriate error
    message based on the reason for the failure.

    :param post_id: The ID of the post containing the comment to be deleted.
    :type post_id: int
    :param comment_id: The ID of the comment to be deleted.
    :type comment_id: int
    :return: A JSON response containing the success status and a message.
    :rtype: tuple
    """
    forum_service = ForumService(app.logger)
    try:
        user_id = g.user_id  # Ensure the user deleting the comment is authorized
        success = forum_service.delete_comment(post_id, comment_id, user_id)
        if success:
            return (
                jsonify({"success": True, "message": "Comment deleted successfully"}),
                200,
            )
        return (
            jsonify({"success": False, "message": "Comment not found or unauthorized"}),
            404,
        )
    except Exception as e:
        app.logger.error(f"Error deleting comment {comment_id} for post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500


@forum_bp.route("/posts/<int:post_id>/comments", methods=["DELETE"])
@jwt_required
def delete_all_comments(post_id):
    """
    Deletes all comments associated with a specified post.

    This endpoint is responsible for removing all comments corresponding to the given post
    ID. It leverages a forum service to perform the deletion and handles the response in
    accordance with the outcome, including success, no comments found, or an internal
    server error.

    :method: DELETE

    :param post_id: The unique identifier of the post whose comments are to be deleted.
    :type post_id: int

    :return: A JSON response indicating the success status and corresponding message of
        the operation.
    :rtype: flask.Response
    """
    forum_service = ForumService(app.logger)
    try:
        success = forum_service.delete_all_comments(post_id)
        if success:
            return (
                jsonify(
                    {"success": True, "message": "All comments deleted successfully"}
                ),
                200,
            )
        return (
            jsonify({"success": False, "message": "No comments found for the post"}),
            404,
        )
    except Exception as e:
        app.logger.error(f"Error deleting comments for post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500
