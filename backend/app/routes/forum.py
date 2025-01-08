from flask import Blueprint
from flask import current_app as app
from flask import g, jsonify, request

from ..services.forumservice import ForumService
from ..utils.auth import jwt_required

forum_bp = Blueprint("forum_api", __name__, url_prefix="/api/forum")




@forum_bp.route("/posts", methods=["GET"])
def list_posts():
    """
    Fetch all forum posts.
    """
    # Instantiate ForumService
    forum_service = ForumService(app.logger)
    try:
        posts = forum_service.get_all_posts()
        return jsonify({"success": True, "posts": posts}), 200
    except Exception as e:
        app.logger.error(f"Error fetching posts: {e}")
        return jsonify({"success": False, "message": "Failed to fetch posts"}), 500


@forum_bp.route("/posts/<int:post_id>", methods=["GET"])
def view_post(post_id):
    """
    Fetch a single forum post and its comments.
    """
    # Instantiate ForumService
    forum_service = ForumService(app.logger)
    try:
        post = forum_service.get_post_by_id(post_id)
        if not post:
            return jsonify({"success": False, "message": "Post not found"}), 404

        comments = forum_service.get_post_comments(post_id)
        return jsonify({"success": True, "post": post, "comments": comments}), 200
    except Exception as e:
        app.logger.error(f"Error fetching post {post_id}: {e}")
        return jsonify({"success": False, "message": "Failed to fetch post"}), 500


@forum_bp.route("/posts", methods=["POST"])
@jwt_required
def create_post():
    """
    Create a new forum post.
    """
    # Instantiate ForumService
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return (
                jsonify(
                    {"success": False, "message": "Title and content are required"}
                ),
                400,
            )

        user_id = g.user_id
        post = forum_service.create_post(user_id, {"title": title, "content": content})
        if post:
            return jsonify({"success": True, "title": post["title"], "content": content}), 201
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
    # Instantiate ForumService
    forum_service = ForumService(app.logger)
    try:
        data = request.json
        content = data.get("content")

        if not content:
            return jsonify({"success": False, "message": "Content is required"}), 400

        user_id = g.user_id
        comment = forum_service.add_comment_to_post(
            user_id, post_id, {"content": content}
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
    # Instantiate ForumService
    forum_service = ForumService(app.logger)
    try:
        user_id = g.user_id
        success = forum_service.delete_post(post_id, user_id)
        if success:
            return (
                jsonify({"success": True, "message": "Post deleted successfully"}),
                200,
            )
        return jsonify({"success": False, "message": "Failed to delete post"}), 400
    except Exception as e:
        app.logger.error(f"Error deleting post {post_id}: {e}")
        return jsonify({"success": False, "message": "An internal error occurred"}), 500
