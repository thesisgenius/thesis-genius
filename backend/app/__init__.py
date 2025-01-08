from flask import Flask
from flask_cors import CORS

from .utils.db import database_proxy, initialize_database

from .routes import register_routes


def create_app(config_name="development"):
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    # Initialize database

    initialize_database(app)

    # Enable CORS
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