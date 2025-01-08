import os
from backend import create_app


def main():
    """
    Entry point to start the Flask application.
    """
    try:
        app = create_app()
        app.logger.info(f"Starting Flask server in {os.environ['FLASK_ENV']} environment")
        app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 8557)))
    except Exception as e:
        print(f"Failed to start the application: {e}")
        raise
