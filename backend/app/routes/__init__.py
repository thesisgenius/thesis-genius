from flask import jsonify, request  # Added imports
from flask_cors import CORS

from .auth import auth_bp
from .format import format_bp
from .forum import forum_bp
from .status import status_bp
from .thesis import thesis_bp
from .user import user_bp


def register_routes(app):
    """
    Register all blueprints with the Flask app.
    """
    try:
        CORS(
            app,
            resources={r"/*": {"origins": "*"}},
            supports_credentials=True,
            allow_headers=["Authorization", "Content-Type"],
            expose_headers=["Authorization", "Content-Type"],
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        )

        @app.before_request  # Fixed placement of function definition
        def handle_options():
            if request.method == "OPTIONS":
                response = jsonify()
                response.status_code = 200
                response.headers["Access-Control-Allow-Origin"] = request.headers.get(
                    "Origin", "*"
                )
                response.headers["Access-Control-Allow-Methods"] = (
                    "GET, POST, PUT, DELETE, OPTIONS"
                )
                response.headers["Access-Control-Allow-Headers"] = (
                    "Authorization, Content-Type"
                )
                response.headers["Access-Control-Allow-Credentials"] = "true"
                return response

        app.register_blueprint(status_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(thesis_bp)
        app.register_blueprint(forum_bp)
        app.register_blueprint(format_bp)
    except Exception as e:
        app.logger.error(f"Failed to register blueprints: {e}")
        raise
