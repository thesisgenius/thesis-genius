from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.data import Role, User
from ..utils.auth import generate_token
from ..utils.redis_helper import blacklist_token

DEFAULT_ROLE = "Student"
ADMIN_ROLE = "Admin"


class UserService:
    def __init__(self, logger):
        """Initialize the UserService with a logger instance."""
        self.logger = logger

    # --- Reusable Helpers ---
    def _get_user_by_email(self, email):
        user = User.get_or_none(User.email == email)
        if not user:
            self.logger.warning(f"User with email {email} not found.")
        return user

    def _get_user_by_id(self, user_id):
        user = User.get_or_none(User.id == user_id)
        if not user:
            self.logger.warning(f"User with ID {user_id} not found.")
        return user

    def _get_role(self, role_name):
        role = Role.get_or_none(Role.name == role_name)
        if not role:
            self.logger.error(f"Role '{role_name}' does not exist.")
        return role

    # --- Main Service Methods ---
    def authenticate_user(self, email, password):
        """Authenticate a user by their email and password."""
        try:
            user = self._get_user_by_email(email)
            if not user or not user.is_active:
                return None

            if check_password_hash(user.password, password):
                self.logger.info(f"User {user.id} authenticated successfully.")
                return model_to_dict(user)

            self.logger.warning(f"Authentication failed for email: {email}")
            return None
        except Exception as e:
            self.logger.error(f"Error during authentication: {e}")
            return None

    def create_user(
        self,
        first_name,
        last_name,
        email,
        institution=None,
        password=None,
        role=DEFAULT_ROLE,
        is_active=True,
        is_admin=None,
    ):
        """
        Create a new user with the given details. Raises specific exceptions for errors.
        """
        try:
            # Ensure institution has a valid default
            if institution is None:
                institution = "Unknown Institution"

            # Ensure the role exists
            role_obj = self._get_role(role)
            if not role_obj:
                self.logger.error(f"Cannot create user: Role '{role}' does not exist.")
                raise ValueError(f"Role '{role}' not found.")

            # Infer is_admin from role if not explicitly provided
            if is_admin is None:
                is_admin = role == ADMIN_ROLE

            # Hash the password
            hashed_password = generate_password_hash(password)

            # Create the user
            user = User.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email,  # Ensure username matches email unless specified
                institution=institution,
                password=hashed_password,
                role=role_obj,
                is_active=is_active,
                is_admin=is_admin,
            )
            user.save()
            self.logger.info(f"User created successfully: {user.id}")
            return user  # Return the user object for further use if needed

        except IntegrityError as e:
            # Handle duplicate email/username gracefully
            if "UNIQUE constraint failed" in str(e):
                self.logger.warning(f"Duplicate user creation attempted: {e}")
                raise IntegrityError(
                    "A user with this email or username already exists."
                )
            else:
                self.logger.error(f"IntegrityError during user creation: {e}")
                raise

        except Exception as e:
            # Handle general errors
            self.logger.error(f"Error creating user: {e}")
            raise

    def fetch_user_data(self, user_id):
        """Fetch user data for the given user ID."""
        try:
            user = self._get_user_by_id(user_id)
            if not user:
                return None

            user_data = model_to_dict(user)
            if "role" in user_data:
                user_data["role"] = model_to_dict(user.role)

            self.logger.info(f"User {user_id} data fetched successfully.")
            return user_data
        except Exception as e:
            self.logger.error(f"Error fetching user data: {e}")
            return None

    def update_user(self, user_id, updates):
        """Update user profile data."""
        try:
            updated_rows = User.update(**updates).where(User.id == user_id).execute()
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

    def change_user_status(self, user_id, is_active, token=None):
        """Change the status of a user and optionally blacklist their token."""
        try:
            # Fetch the user by id
            user = self._get_user_by_id(user_id)

            # Abort if the user does not exist
            if not user:
                self.logger.warning(f"User {user_id} not found.")
                from flask import abort

                abort(404, description="User not found.")
                return  # Explicitly stop execution (not really needed, but for clarity)

            # If the user is already in the desired active/inactive state
            if user.is_active == is_active:
                status = "active" if is_active else "inactive"
                self.logger.info(f"User {user_id} is already {status}.")
                return False

            # Update and save the user's status
            user.is_active = is_active
            user.save()

            # Invalidate the token if provided and the user is deactivated
            if token and not is_active:
                blacklist_token(token)
                self.logger.info(f"JWT token invalidated for user {user_id}.")

            # Log a success message
            action = "activated" if is_active else "deactivated"
            self.logger.info(f"User {user_id} {action} successfully.")
            return True

        except Exception as error:
            # Log and abort for unexpected issues
            self.logger.error(f"Error changing status for user {user_id}: {error}")
            from flask import abort

            abort(500, description="Internal server error.")

    def logout(self, user_id, token):
        """Log out the user by invalidating their current session."""
        try:
            user = self._get_user_by_id(user_id)
            if not user:
                self.logger.warning(f"Logout failed: User with ID {user_id} not found.")
                from flask import abort

                abort(404, description="User not found.")

            blacklist_token(token)
            self.logger.info(
                f"User {user_id} logged out successfully, JWT token invalidated."
            )
            return True
        except Exception as e:
            self.logger.error(f"Error logging out user {user_id}: {e}")
            from flask import abort

            abort(500, description="Internal server error.")

    def generate_token(self, user_id):
        """Generate a JWT token for the specified user ID."""
        try:
            token = generate_token(user_id)
            self.logger.info(f"Token generated for user {user_id}.")
            return token
        except Exception as e:
            self.logger.error(f"Error generating token for user {user_id}: {e}")
            return None
