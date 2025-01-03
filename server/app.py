import os
import sys
from dotenv import load_dotenv

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from server import create_app
if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 8557)))
