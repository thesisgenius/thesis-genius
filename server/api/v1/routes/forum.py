# api/v1/routes/forum.py
from flask import Blueprint, jsonify, request

from server import db
from server.models.forum import Forum

forum_bp_v1 = Blueprint("forum_v1", __name__, url_prefix="/forum")


@forum_bp_v1.route("/", methods=["GET"])
def get_forum():
    return jsonify({"message": "Welcome to ThesisGenius Forum!"}), 200


@forum_bp_v1.route("/posts", methods=["GET"])
def get_forums():
    forums = db.session.query(Forum).all()
    return (
        jsonify(
            [
                {
                    "id": forum.id,
                    "user_id": forum.user_id,
                    "title": forum.title,
                    "description": forum.description,
                    "body": forum.body,
                    "created_at": forum.created_at,
                }
                for forum in forums
            ]
        ),
        200,
    )


@forum_bp_v1.route("/posts/<int:forum_id>", methods=["GET"])
def get_forum_with_id(forum_id):
    forum = db.session.get(Forum, forum_id)
    if not forum:
        return jsonify({"error": "Forum not found"}), 404
    return (
        jsonify(
            {
                "id": forum.id,
                "user_id": forum.user_id,
                "title": forum.title,
                "description": forum.description,
                "body": forum.body,
                "created_at": forum.created_at,
            }
        ),
        200,
    )


@forum_bp_v1.route("/posts", methods=["POST"])
def create_forum():
    data = request.get_json()
    if not data or "user_id" not in data or "title" not in data or "body" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_forum = Forum(
        user_id=data["user_id"],
        title=data["title"],
        description=data.get("description"),
        body=data["body"],
    )
    db.session.add(new_forum)
    db.session.commit()

    return jsonify({"message": "Forum created", "forum_id": new_forum.id}), 201


@forum_bp_v1.route("/posts/<int:forum_id>", methods=["PUT"])
def update_forum(forum_id):
    forum = db.session.get(Forum, forum_id)
    if not forum:
        return jsonify({"error": "Forum not found"}), 404

    data = request.get_json()
    if "title" in data:
        forum.title = data["title"]
    if "description" in data:
        forum.description = data["description"]
    if "body" in data:
        forum.body = data["body"]

    db.session.commit()
    return jsonify({"message": "Forum updated"}), 200


@forum_bp_v1.route("/posts/<int:forum_id>", methods=["DELETE"])
def delete_forum(forum_id):
    forum = db.session.get(Forum, forum_id)
    if not forum:
        return jsonify({"error": "Forum not found"}), 404

    db.session.delete(forum)
    db.session.commit()
    return jsonify({"message": "Forum deleted"}), 200
