from flask import Blueprint, current_app as app, g, jsonify, request
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

        posts_data = forum_service.get_all_posts(page=page, per_page=per_page, order_by=order_by)
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
        post = forum_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"success": False, "message": "Post not found"}), 404

        # Pagination for comments
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        comments_data = forum_service.get_post_comments(post_id, page=page, per_page=per_page)
        return jsonify({"success": True, "post": post, "comments": comments_data}), 200
    except Exception as e:
        app.logger.error(f"Error fetching post {post_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch post"}), 500


@forum_bp.route("/posts", methods=["POST"])
@jwt_required
def create_post():
    """
    Create a new forum post.
    """
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        if not data or "title" not in data or "content" not in data:
            return jsonify({"success": False, "message": "Title and content are required"}), 400

        user_id = g.user_id
        post = forum_service.create_post(user_id, {"title": data["title"], "content": data["content"]})
        if post:
            return jsonify({"success": True, "post": data["title"], "user": user_id, "id": post["id"]}), 201
        return jsonify({"success": False, "message": "Failed to create post"}), 400
    except Exception as e:
        app.logger.error(f"Error creating post: {e}")
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
        comment = forum_service.add_comment_to_post(user_id, post_id, {"content": data["content"]})
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
            return jsonify({"success": True, "message": "Post deleted successfully"}), 200
        return jsonify({"success": False, "message": "Post not found or unauthorized"}), 404
    except Exception as e:
        app.logger.error(f"Error deleting post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500
