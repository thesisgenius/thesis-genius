import os
import sys
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from config import config_dict



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Initialize extensions
db = SQLAlchemy()

def create_app():
    load_dotenv()
    """Application Factory Pattern."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_dict["development"])

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Import and register the v1 API Blueprint dynamically
    from server.api.v1 import v1
    app.register_blueprint(v1, url_prefix="/v1/api")

    # Create database tables within the application context
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
