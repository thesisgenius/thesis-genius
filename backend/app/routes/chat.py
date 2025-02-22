import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


# Initialize Flask Blueprint
chat_bp = Blueprint("chat_api", __name__, url_prefix="/api/chat")
CORS(chat_bp)  # Enable CORS for frontend requests

# Configure Gemini API
API_KEY = os.getenv("API_KEY") 
genai.configure(api_key=API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
chat_history = model.start_chat(history=[])

# Send Initial AI Instruction (This is sent once and ignored in responses)
INITIAL_MESSAGE = (
    "Do not use *, **, or *** unless it is part of natural formatting. "
    "Avoid unusual text styles unless explicitly requested."
)
chat_history.send_message(INITIAL_MESSAGE)  # This does not expect a response


@chat_bp.route("/", methods=["POST"])
def chat():
    """Handle chat requests from frontend"""
    try:
        # Get user question from request
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"success": False, "response": "No question provided."}), 400

        # Send the message to Gemini AI with history tracking
        response = chat_history.send_message(question)
        ai_response = response.text.strip() if response.text else "No response from AI."

        # Return the AI response
        return jsonify({"success": True, "response": ai_response})

    except Exception as e:
        return jsonify({"success": False, "response": f"Error: {str(e)}"}), 500
