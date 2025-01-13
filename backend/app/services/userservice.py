from peewee import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.data import User
from ..utils.auth import generate_token
from ..utils.db import model_to_dict


class UserService:
    def __init__(self, logger):
        """
        Initialize the UserService with a logger instance.
        """
        self.logger = logger

    def authenticate_user(self, email, password):
        """
        Authenticate a user by their email and password.
        """
        try:
            user = User.get_or_none(User.email == email)
            if not user:
                self.logger.warning(f"User with email {email} not found.")
                return None

            if not user.is_active:
                self.logger.warning(f"User {user.id} is deactivated.")
                return None

            if check_password_hash(user.password, password):
                self.logger.info(f"User {user.id} authenticated successfully.")
                return model_to_dict(user)

            self.logger.warning(f"Authentication failed for email: {email}")
            return None
        except Exception as e:
            self.logger.error(f"Error during authentication: {e}")
            return None

    def create_user(self, name, email, password):
        """
        Create a new user with the given name, email, and password.
        """
        try:
            hashed_password = generate_password_hash(password)
            user = User.create(name=name, email=email, password=hashed_password)
            self.logger.info(f"User created successfully: {user.id}")
            return True
        except IntegrityError:
            self.logger.warning(f"User creation failed: Email {email} already exists.")
            return False
        except Exception as e:
            self.logger.error(f"Error creating user: {e}")
            return False

    def get_user_data(self, user_id):
        """
        Fetch user data by ID.
        """
        try:
            user = User.get_or_none(User.id == user_id)
            if user:
                self.logger.info(f"User {user.id} data fetched successfully.")
                return model_to_dict(user)  # Return the user as a dictionary
            self.logger.warning(f"User with ID {user_id} not found.")
            return None
        except Exception as e:
            self.logger.error(f"Error fetching user data for ID {user_id}: {e}")
            return None

    def update_user_data(self, user_id, update_data):
        """
        Update user profile data.
        """
        try:
            query = User.update(**update_data).where(User.id == user_id)
            updated_rows = query.execute()
            if updated_rows > 0:
                self.logger.info(f"User {user_id} updated successfully.")
                return True
            self.logger.warning(f"No rows updated for user {user_id}.")
            return False
        except IntegrityError as e:
            self.logger.error(f"IntegrityError updating user {user_id}: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating user {user_id}: {e}")
            return False

    def deactivate_user(self, user_id, token):
        """
        Deactivate a user account by setting is_active to False.
        """
        try:
            user = User.get_or_none(User.id == user_id)
            if not user:
                self.logger.warning(f"User with ID {user_id} not found.")
                return False

            from ..utils.redis_helper import blacklist_token
            blacklist_token(token)
            self.logger.info(f"User {user_id} logged out successfully, JWT token invalidated.")

            user.is_active = False
            user.save()
            self.logger.info(f"User {user_id} deactivated successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error deactivating user {user_id}: {e}")
            return False

    def activate_user(self, user_id):
        """
        Reactivate a user account by setting is_active to True.
        """
        try:
            user = User.get_or_none(User.id == user_id)
            if not user:
                self.logger.warning(f"User with ID {user_id} not found.")
                return False

            user.is_active = True
            user.save()
            self.logger.info(f"User {user_id} activated successfully.")
            return True
        except Exception as e:
            self.logger.error(f"Error activating user {user_id}: {e}")
            return False

    def generate_token(self, user_id):
        """
        Generate a JWT token for the specified user ID.
        """
        try:
            token = generate_token(user_id)
            self.logger.info(f"Token generated for user {user_id}.")
            return token
        except Exception as e:
            self.logger.error(f"Error generating token for user {user_id}: {e}")
            return None

    def logout(self, user_id, token):
        """
        Log out the user by invalidating their current session.
        """
        try:
            user = User.get_or_none(User.id == user_id)
            if not user:
                self.logger.warning(f"Logout failed: User with ID {user_id} not found.")
                return False

            from ..utils.redis_helper import blacklist_token
            blacklist_token(token)
            self.logger.info(f"User {user_id} logged out successfully, JWT token invalidated.")
            return True
        except Exception as e:
            self.logger.error(f"Error logging out user {user_id}: {e}")
            return False