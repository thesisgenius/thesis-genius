from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
DB = SQLAlchemy(app)
CORS(app)

# Importing routes
from routes.api import api_bp
app.register_blueprint(api_bp, url_prefix="/api")

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Thesis Writing API!"})

if __name__ == "__main__":
    app.run(debug=True)
