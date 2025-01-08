import os
from dotenv import load_dotenv
from app import create_app



if __name__ == "__main__":
    """
    Entry point to start the Flask application.
    """
    try:
        load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
        runtime_env = os.getenv("FLASK_ENV")
        app = create_app(runtime_env)
        app.logger.info(
            f"Starting Flask server in {runtime_env} environment"
        )
        app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 8557)))
    except Exception as e:
        print(f"Failed to start the application: {e}")
        raise
