from flask import Blueprint, jsonify, request
from server.models.thesis import Thesis
from server.app import db

thesis_bp_v1 = Blueprint("thesis_v1", __name__)

# Get all theses
@thesis_bp_v1.route("/thesis", methods=["GET"])
def get_theses():
    theses = Thesis.query.all()
    theses_list = [{"id": t.id, "title": t.title, "content": t.content} for t in theses]
    return jsonify(theses_list)


# Add a new thesis
@thesis_bp_v1.route("/thesis", methods=["POST"])
def add_thesis():
    data = request.json
    new_thesis = Thesis(title=data["title"], content=data["content"])
    db.session.add(new_thesis)
    db.session.commit()
    return jsonify({"message": "Thesis added successfully!"}), 201
