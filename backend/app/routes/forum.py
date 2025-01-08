from flask import Blueprint, request, render_template, flash, redirect, url_for, g
from backend import ForumService
from backend import jwt_required

forum_bp = Blueprint(
    "forum_api",
    __name__,
    url_prefix="/api/v1/forum",
    template_folder="templates",
    static_folder="static",
)

forum_service = ForumService()

@forum_bp.route("/forum", methods=["GET"])
def list_posts():
    """
    Display all forum posts.
    """
    posts = forum_service.get_all_posts()
    return render_template("forum/list.html", posts=posts)


@forum_bp.route("/forum/<int:post_id>", methods=["GET"])
def view_post(post_id):
    """
    View a single forum post and its comments.
    """
    post = forum_service.get_post_by_id(post_id)
    if not post:
        flash("Post not found.", "error")
        return redirect(url_for("forum_api.list_posts"))

    comments = forum_service.get_post_comments(post_id)
    return render_template("forum/view.html", post=post, comments=comments)


@forum_bp.route("/forum/create", methods=["GET", "POST"])
@jwt_required
def create_post():
    """
    Create a new forum post.
    """
    user_id = g.user_id
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        post_data = {"title": title, "content": content}
        post = forum_service.create_post(user_id, post_data)

        if post:
            flash("Post created successfully!", "success")
            return redirect(url_for("forum_api.list_posts"))
        else:
            flash("Failed to create post. Please try again.", "error")

    return render_template("forum/create.html")


@forum_bp.route("/forum/<int:post_id>/comment", methods=["POST"])
@jwt_required
def add_comment(post_id):
    """
    Add a comment to a forum post.
    """
    user_id = g.user_id
    content = request.form["content"]
    comment_data = {"content": content}
    comment = forum_service.add_comment_to_post(user_id, post_id, comment_data)

    if comment:
        flash("Comment added successfully!", "success")
    else:
        flash("Failed to add comment. Please try again.", "error")

    return redirect(url_for("forum_api.view_post", post_id=post_id))


@forum_bp.route("/forum/<int:post_id>/delete", methods=["POST"])
@jwt_required
def delete_post(post_id):
    """
    Delete a forum post.
    """
    user_id = g.user_id
    success = forum_service.delete_post(post_id, user_id)
    if success:
        flash("Post deleted successfully.", "success")
    else:
        flash("Failed to delete post. Please try again.", "error")

    return redirect(url_for("forum_api.list_posts"))
