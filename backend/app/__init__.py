from flask import Flask
from flask_cors import CORS

from .routes import register_routes
from .utils.db import database_proxy, initialize_database


def create_app(config_name="testing"):
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    # Initialize database

    initialize_database(app)

    # Enable CORS for frontend development
    CORS(app)

    # Register API routes
    register_routes(app)

    # Ensure the database connection is closed after each request
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if not database_proxy.is_closed():
            database_proxy.close()
            app.logger.info("Database connection closed.")

    return app
