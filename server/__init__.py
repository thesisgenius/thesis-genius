import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from tenacity import retry, stop_after_attempt, wait_fixed
import argparse
from server.config import config_dict

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

# Command-line argument parser for log level
from server.utils.log import get_logger
parser = argparse.ArgumentParser(description="Run the application with configurable logging.")
parser.add_argument(
    "--log-level",
    type=str,
    default="INFO",
    help="Set the logging level (DEBUG, INFO, WARNING, ERROR)."
)
args = parser.parse_args()
# Initialize the logger with the provided log level
logger = get_logger(__name__, args.log_level)


def initialize_dev_db():
    logger.info("Initializing development database...")
    from server.models.db import DBManager

    logger.info("Initializing database manager...")
    db_manager = DBManager(root_password=os.environ.get("DEV_DB_ROOT_PW"))

    logger.info("Connecting to database...")
    db_manager.connect()
    if not db_manager.connection:
        logger.error("Failed to connect to database!")
        return
    else:
        logger.info("Connected to database!")

    logger.info("Creating database thesis_app_dev...")
    db_manager.create_database("thesis_app_dev")
    logger.info("Created database thesis_app_dev!")

    logger.info("Creating user...")
    db_manager.create_user("thesis_dev", "dev_password","thesis_app_dev")


    db_manager.execute_sql_file("server/models/db/schema.sql")

    db_manager.close_connection()
    logger.info("Database initialization complete!")



# Retry mechanism for database connection
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def db_init(app):
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        try:
            logger.info("Attempting database initialization...")
            db.init_app(app)
            logger.info("Attempting database initial migration...")
            migrate.init_app(app, db)
            with app.app_context():
                # Test the connection
                logger.info("Attempting to connect to database...")
                db.engine.connect()
                logger.info("Database connection successful!")
        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            raise


def create_app():
    """Application Factory Pattern."""
    api_app = Flask(__name__)

    logger.info(f"Starting {os.environ['FLASK_ENV']} environment...")
    api_app.config.from_object(config_dict[os.environ["FLASK_ENV"]])

    # Check if running in development environment
    if os.environ["FLASK_ENV"] == "development":
        initialize_dev_db()

    # Initialize SQLAlchemy with the app
    logger.info("Initializing ThesisGenius application database")
    db_init(api_app)

    # Import and register the v1 API Blueprint dynamically
    logger.info("Registering v1 API routes (/v1/api)")
    from server.api.v1 import v1

    api_app.register_blueprint(v1, url_prefix="/v1/api")

    return api_app
