from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from server.config import config_dict

# Initialize extensions
db = SQLAlchemy()

load_dotenv()


def create_app():
    """Application Factory Pattern."""
    api_app = Flask(__name__)

    # Load configuration
    import os

    api_app.config.from_object(config_dict[os.environ["FLASK_ENV"]])

    # Initialize SQLAlchemy with the app
    db.init_app(api_app)

    # Import and register the v1 API Blueprint dynamically
    from server.api.v1 import v1

    api_app.register_blueprint(v1, url_prefix="/v1/api")

    # Create database tables within the application context
    with api_app.app_context():
        db.create_all()

    return api_app
