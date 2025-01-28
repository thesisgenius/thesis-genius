from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.forumservice import ForumService
from ..utils.auth import jwt_required

forum_bp = Blueprint("forum_api", __name__, url_prefix="/api/forum")


@forum_bp.route("/posts", methods=["GET"])
def list_posts():
    """
    Fetch all forum posts with pagination.
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
    Fetch a single forum post and its comments with pagination.
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
        return jsonify({
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
            "comments": comments_data
        }), 200
    except Exception as e:
        app.logger.error(f"Error fetching post {post_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch post"}), 500



@forum_bp.route("/posts/new", methods=["POST"])
@jwt_required
def create_post():
    """
    Create a new forum post.
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
    Update an existing forum post.
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or ("title" not in data and "content" not in data):
            return jsonify({"success": False, "message": "Title or content is required"}), 400

        user_id = g.user_id  # Ensure the user is authorized to update the post
        success = forum_service.update_post(post_id, data, user_id)
        if success:
            return jsonify({"success": True, "message": "Post updated successfully"}), 200
        return jsonify({"success": False, "message": "Post not found or unauthorized"}), 404
    except Exception as e:
        app.logger.error(f"Error updating post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500



@forum_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required
def add_comment(post_id):
    """
    Add a comment to a forum post.
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
    Delete a forum post.
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
    Fetch a single comment by ID for a specific post.
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
    Update a specific comment by ID for a given post.
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
    Delete a specific comment by ID for a given post.
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
    Delete all comments for a specific post.
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
