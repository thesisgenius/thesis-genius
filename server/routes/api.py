from flask import Blueprint, jsonify, request
from models.thesis import Thesis
from ..app import DB

api_bp = Blueprint("api", __name__)

# Get all theses
@api_bp.route("/thesis", methods=["GET"])
def get_theses():
    theses = Thesis.query.all()
    theses_list = [{"id": t.id, "title": t.title, "content": t.content} for t in theses]
    return jsonify(theses_list)


# Add a new thesis
@api_bp.route("/thesis", methods=["POST"])
def add_thesis():
    data = request.json
    new_thesis = Thesis(title=data["title"], content=data["content"])
    DB.session.add(new_thesis)
    DB.session.commit()
    return jsonify({"message": "Thesis added successfully!"}), 201
