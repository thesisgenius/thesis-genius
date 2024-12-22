# api/v1/routes/forum.py
from flask import Blueprint

forum_bp_v1 = Blueprint("forum_v1", __name__)


@forum_bp_v1.route("/forum", methods=["GET"])
def get_forum():
    return {"message": "v1 forum endpoint"}
