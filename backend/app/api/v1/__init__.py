from flask import Blueprint

from backend.api.v1.routes.auth import auth_bp
from backend.api.v1.routes.forum import forum_bp
from backend.api.v1.routes.thesis import thesis_bp
from backend.api.v1.routes.user import user_bp

v1 = Blueprint("v1_api", __name__, url_prefix="/api/v1")
v1.register_blueprint(thesis_bp, url_prefix="/thesis")
v1.register_blueprint(user_bp, url_prefix="/user")
v1.register_blueprint(forum_bp, url_prefix="/forum")
v1.register_blueprint(auth_bp, url_prefix="/auth")
