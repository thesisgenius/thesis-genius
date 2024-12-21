from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
DB = SQLAlchemy(app)
CORS(app)

# Importing routes
from api.v1 import v1 as v1_blueprint
app.register_blueprint(v1_blueprint)


if __name__ == "__main__":
    app.run(debug=True)
