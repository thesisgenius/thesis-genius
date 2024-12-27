from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from server import db
from server.models.thesis import Thesis

thesis_bp_v1 = Blueprint("thesis_v1", __name__, url_prefix="/thesis")


# Create Thesis
@thesis_bp_v1.route("/", methods=["POST"])
def create_thesis():
    data = request.get_json()
    if not data:
        abort(400, description="Invalid request payload.")

    title = data.get("title")
    author = data.get("author")
    abstract = data.get("abstract")
    status = data.get("status", "In Progress")
    submission_date = data.get("submission_date")

    if not title or not author:
        abort(400, description="Title and Author are required.")

    try:
        submission_date = (
            datetime.strptime(submission_date, "%Y-%m-%d").date()
            if submission_date
            else None
        )
        thesis = Thesis(
            title=title,
            author=author,
            abstract=abstract,
            status=status,
            submission_date=submission_date,
        )
        db.session.add(thesis)
        db.session.commit()
        return (
            jsonify({"id": thesis.id, "message": "Thesis created successfully."}),
            201,
        )
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))


# Retrieve All Theses
@thesis_bp_v1.route("/all", methods=["GET"])
def get_all_theses():
    theses = Thesis.query.all()
    return jsonify(
        [
            {
                "id": thesis.id,
                "title": thesis.title,
                "author": thesis.author,
                "abstract": thesis.abstract,
                "status": thesis.status,
                "submission_date": (
                    thesis.submission_date.strftime("%Y-%m-%d")
                    if thesis.submission_date
                    else None
                ),
            }
            for thesis in theses
        ]
    )


# Retrieve Single Thesis
@thesis_bp_v1.route("/<int:id>", methods=["GET"])
def get_thesis(id):
    thesis = db.session.get(Thesis, id)
    if not thesis:
        abort(404, description="Thesis not found.")
    return jsonify(
        {
            "id": thesis.id,
            "title": thesis.title,
            "author": thesis.author,
            "abstract": thesis.abstract,
            "status": thesis.status,
            "submission_date": (
                thesis.submission_date.strftime("%Y-%m-%d")
                if thesis.submission_date
                else None
            ),
        }
    )


# Update Thesis
@thesis_bp_v1.route("/<int:id>", methods=["PUT"])
def update_thesis(id):
    thesis = db.session.get(Thesis, id)
    if not thesis:
        abort(404, description="Thesis not found.")

    data = request.get_json()
    if not data:
        abort(400, description="Invalid request payload.")

    try:
        thesis.title = data.get("title", thesis.title)
        thesis.author = data.get("author", thesis.author)
        thesis.abstract = data.get("abstract", thesis.abstract)
        thesis.status = data.get("status", thesis.status)
        if "submission_date" in data:
            thesis.submission_date = (
                datetime.strptime(data["submission_date"], "%Y-%m-%d").date()
                if data["submission_date"]
                else None
            )
        db.session.commit()
        return jsonify({"message": "Thesis updated successfully."})
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))


# Delete Thesis
@thesis_bp_v1.route("/<int:id>", methods=["DELETE"])
def delete_thesis(id):
    thesis = db.session.get(Thesis, id)
    if not thesis:
        abort(404, description="Thesis not found.")

    try:
        db.session.delete(thesis)
        db.session.commit()
        return jsonify({"message": "Thesis deleted successfully."})
    except Exception as e:
        db.session.rollback()
        abort(500, description=str(e))
