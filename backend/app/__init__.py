import os
from flask import Flask
from dotenv import load_dotenv
from .routes import register_routes
from .models.data import initialize_database
from .services.dbservice import DBService
from backend.config import config_dict
from .utils.log import get_logger



def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file
    app.config.from_object(config_dict[os.environ["FLASK_ENV"]])

    # Initialize logger
    logger = get_logger(__name__, os.environ.get("LOG_LEVEL"))
    app.logger = logger

    # Initialize database
    db = initialize_database(app.config)  # Pass config explicitly
    db_service = DBService(app)

    with app.app_context():
        app.logger.info("Initializing database...")
        db_service.initialize()
        db_service.load_settings()

    # Register API routes
    register_routes(app)

    # Apply middleware
    from .utils.auth import jwt_required, load_user

    @app.before_request
    def apply_user_middleware():
        """
        Middleware to load user details into `g` context for authenticated routes.
        """
        jwt_required(lambda: None)()  # Validate JWT token
        load_user()  # Load user into `g.user`

    # Ensure database connection is closed after each request
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        db_service.close_connection()

    app.logger.info("App initialized successfully.")
    return app
