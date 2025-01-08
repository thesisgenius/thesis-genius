import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app as app
from datetime import datetime, timezone, timedelta
from backend import User

class UserService:
    def __init__(self):
        pass

    def login(self, email, password):
        """
        Authenticate a user and return a JWT token if successful.
        """
        user = User.get_or_none(User.email == email)
        if not user or not check_password_hash(user.password, password):
            app.logger.warning("Invalid credentials for user login")
            return None  # Return None if authentication fails

        # Generate JWT token
        token = self.generate_token(user.id)
        app.logger.info(f"User {user.id} logged in successfully.")
        return token

    def logout(self, user_id):
        """
        Placeholder for logout logic.
        """
        app.logger.info(f"User {user_id} logged out.")
        # For JWT-based authentication, logout is client-side (invalidate the token locally).

    def get_user_data(self, user_id):
        """
        Fetch user data by ID.
        """
        try:
            user = User.get_by_id(user_id)
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        except User.DoesNotExist:
            app.logger.error(f"User with ID {user_id} does not exist.")
            return None

    def get_user_data(self, user_id):
        """
        Fetch user data by ID.
        """
        try:
            user = User.get_by_id(user_id)
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_admin": user.is_admin,
                "created_at": user.created_at,
            }
        except User.DoesNotExist:
            return None

        

    def update_user_data(self, user_id, update_data):
        """
        Update user profile data.
        """
        update_data["updated_at"] = datetime.now(timezone.utc)  # Update timestamp
        query = User.update(**update_data).where(User.id == user_id)
        updated_rows = query.execute()
        return updated_rows > 0  # Return True if any rows were updated

    def create_user(self, name, email, password, is_admin=False):
        """
        Create a new user.
        """
        hashed_password = generate_password_hash(password)
        try:
            User.create(
                name=name,
                email=email,
                password=hashed_password,
                is_admin=is_admin,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            return True
        except Exception as e:
            app.logger.error(f"Error creating user: {e}")
            return False

    def authenticate_user(self, email, password):
        """
        Authenticate a user.
        """
        user = User.get_or_none(User.email == email)
        if user and check_password_hash(user.password, password):
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "is_admin": user.is_admin,
            }
        return None


    # JWT Utilities
    def generate_token(self, user_id):
        """
        Generate a JWT token for the user.
        """
        secret_key = app.config["SECRET_KEY"]  # Access config inside method
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def validate_token(self, token):
        """
        Validate a JWT token and return the user ID if valid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            app.logger.warning("Token has expired.")
            return None
        except jwt.InvalidTokenError:
            app.logger.warning("Invalid token.")
            return None
