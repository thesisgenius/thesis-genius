from flask import Flask, request

from .routes import register_routes
from .utils.db import database_proxy, initialize_database


def create_app(config_name="testing"):
    """
    Creates and configures a Flask application instance with the specified configuration,
    initializes the database, registers API routes, and sets up request lifecycle handlers.

    :param config_name: Name of the configuration to use for the Flask application.
    :type config_name: str, optional
    :return: Configured Flask application instance.
    :rtype: Flask
    """
    app = Flask(__name__)
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")
    # OpenAPI configuration
    app.config.update(
        {
            "APISPEC_TITLE": "ThesisGenius API",
            "APISPEC_VERSION": "v1",
            "APISPEC_SWAGGER_URL": "/docs",
        }
    )

    # Initialize database
    initialize_database(app)

    # Register API routes
    register_routes(app)

    @app.before_request
    def log_request_info():
        app.logger.debug(f"Request Method: {request.method}")
        app.logger.debug(f"Request URL: {request.url}")
        app.logger.debug(f"Request Headers: {request.headers}")
        app.logger.debug(f"Request Body: {request.get_data()}")

    # Ensure the database connection is closed after each request
    @app.teardown_appcontext
    def close_db_connection(exception=None):
        if not database_proxy.is_closed():
            database_proxy.close()
            app.logger.info("Database connection closed.")

    return app
