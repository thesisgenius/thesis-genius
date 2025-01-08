from flask import Blueprint, jsonify, request, render_template, g, current_app as app
from backend.app.services.userservice import UserService
from backend.app.utils.auth import jwt_required

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
    template_folder="templates",
    static_folder="static",
)
user_service = UserService()

@auth_bp.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# Render the signin page (GET)
@auth_bp.route('/signin', methods=['GET'])
def signin_page():
    return render_template('signin.html')

# Handle signin logic (POST)
@auth_bp.route('/signin', methods=['POST'])
def signin():
    """
    API endpoint for user sign-in.
    """
    # Parse JSON payload
    app.logger.info(f"Headers: {request.headers}")
    app.logger.info(f"Payload: {request.get_data()}")
    if not request.is_json:  # Check if the request contains JSON
        return jsonify({"success": False, "message": "Invalid Content-Type. Expected application/json"}), 415

    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Authenticate the user
    user = user_service.authenticate_user(email=email, password=password)
    if user:
        token = user_service.generate_token(user['id'])  # Generate JWT token
        return jsonify({"success": True, "token": token}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401


# Sign-out route (Stateless)
@auth_bp.route('/signout', methods=['POST'])
@jwt_required
def signout():
    user_service.logout(g.user_id)  # Assuming `g.user_id` is set by middleware
    return jsonify({"success": True, "message": "Logged out successfully"}), 200

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    API endpoint for user registration.
    """
    data = request.json  # Parse JSON payload
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Call UserService to handle registration logic
    success = user_service.create_user(name=name, email=email, password=password)
    if success:
        return jsonify({"success": True, "message": "User registered successfully!"}), 201
    else:
        return jsonify({"success": False, "message": "Registration failed. Email might already be in use."}), 400



