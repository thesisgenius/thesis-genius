from .auth import auth_bp
from .forum import forum_bp
from .thesis import thesis_bp
from .user import user_bp


def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    try:
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(thesis_bp)
        app.register_blueprint(forum_bp)
    except Exception as e:
        app.logger.error(f"Failed to register blueprints: {e}")
        raise
