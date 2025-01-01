import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from server import create_app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(host="0.0.0.0", port=port)
