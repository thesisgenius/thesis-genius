from flask import Blueprint
from .routes.thesis import thesis_bp_v1
from .routes.user import user_bp_v1
from .routes.forum import forum_bp_v1

v1 = Blueprint('v1', __name__, url_prefix='/v1/api')
v1.register_blueprint(thesis_bp_v1)
v1.register_blueprint(user_bp_v1)
v1.register_blueprint(forum_bp_v1)
