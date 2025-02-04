from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.data import Role, User
from ..utils.auth import generate_token
from ..utils.redis_helper import blacklist_token

DEFAULT_ROLE = "Student"
ADMIN_ROLE = "Admin"


class UserService:
    """
    Provides services related to user management, authentication, and user status
    updates. This class implements functionalities to handle typical user-related
    operations such as creating a new user, authenticating, updating profile data,
    managing user status, logging out, and generating JWT tokens.

    This is designed to integrate with a database model for storing user and role
    information, as well as handling login sessions and token-based authentication.

    :ivar logger: Instance of a logging framework used for debugging, informational,
        and error logging.
    :type logger: logging.Logger
    """

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
        """
        Authenticates a user by verifying their email and password. This method
        checks whether the provided email corresponds to an active user
        in the database and validates the provided password against the
        stored password hash. If authentication is successful, the user's
        details are returned as a dictionary.

        :param email: The email address of the user to authenticate.
        :type email: str
        :param password: The password of the user to authenticate.
        :type password: str
        :return: A dictionary containing the user's details if authentication
            is successful, or None if authentication fails or any exception
            occurs.
        :rtype: Optional[dict]
        """
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
        username,
        institution=None,
        password=None,
        role=DEFAULT_ROLE,
        is_active=True,
        is_admin=None,
    ):
        """
        Creates a new user with specific parameters such as personal details, credentials, and role. This method
        validates the input, such as ensuring the role exists, hashes the password, and determines admin status
        based on the provided or inferred role. If any error is encountered during the creation process,
        appropriate exceptions will be raised.

        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param email: The email address of the user, used for unique identification.
        :type email: str
        :param username: The username of the user, used for login purposes.
        :type username: str
        :param institution: The institution associated with the user. Defaults to "Unknown Institution" if not provided.
        :type institution: str, optional
        :param password: The plain-text password for the user, which will be hashed before storage.
        :type password: str, optional
        :param role: The role assigned to the user, determining their access rights. Defaults to the application's default role.
        :type role: str
        :param is_active: Indicates whether the user account is active. Defaults to True.
        :type is_active: bool
        :param is_admin: Flags whether the user is an administrator. This will be inferred from the role if not explicitly provided.
        :type is_admin: bool, optional
        :return: The created User object containing all user details.
        :rtype: User
        :raises ValueError: If the specified role does not exist.
        :raises IntegrityError: If there is a unique constraint failure (e.g., duplicate email or username).
        :raises Exception: For general errors during the user creation process.
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
                username=username,
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
        """
        Fetches user data for a given user ID.

        This method retrieves user information from the database using the user ID.
        If the user exists, the data is converted into a dictionary format. If the
        user has a role attribute, the role information is also converted into a
        dictionary and included in the resulting response. Success and error logging
        is performed during the process to provide detailed status updates.

        :param user_id: The unique identifier of the user to fetch data for.
        :type user_id: int
        :return: A dictionary containing user data if the user exists or None if no
            user is found or an error occurs.
        :rtype: dict | None
        """
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
        """
        Updates a user's information in the database based on the given user ID and
        update dictionary. Logs the operation status and handles any exceptions
        that may occur during the update process.

        :param user_id: The ID of the user to be updated.
        :type user_id: int
        :param updates: A dictionary containing the fields and values to be updated
            for the user.
        :type updates: dict
        :return: Returns True if the update was successful, otherwise False.
        :rtype: bool
        :raises IntegrityError: Raised when there is a database integrity constraint
            violation during the update process.
        :raises Exception: Raised for any other errors encountered during the update
            process.
        """
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
        """
        Changes the activation status of a user in the system. This method modifies the
        activation state of a user based on the provided `user_id` and `is_active` parameters.
        Additionally, if a `token` is supplied, it invalidates the token if the user is being
        deactivated.

        :param user_id: The unique identifier of the user whose activation status is
                        to be changed.
        :type user_id: int or str
        :param is_active: A boolean indicating the desired activation state of the user.
                          `True` to activate the user or `False` to deactivate the user.
        :type is_active: bool
        :param token: Optional. The JWT token associated with the user to be invalidated
                      when the user is being deactivated. Expected to be None if no token
                      is to be invalidated.
        :type token: str, optional
        :return: Returns `True` if the user's activation status is successfully changed;
                 returns `False` if the user's status was already in the desired state.
        :rtype: bool
        :raises: 404 if the user with the provided `user_id` is not found,
                 500 in case of unexpected errors during execution.
        """
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
        """
        Logs out a user by invalidating their JWT token.

        This method attempts to log out the user specified by their unique identifier
        (user_id) by invalidating the provided JWT token. It retrieves the user from
        the database and ensures they exist before performing the logout action. If the
        logout process is successful, the token is blacklisted, effectively preventing
        it from being used for subsequent requests.

        In case of errors during the process, appropriate HTTP responses are triggered.

        :param user_id: Unique identifier of the user.
        :type user_id: int
        :param token: JWT token to be invalidated.
        :type token: str
        :return: True if the user was logged out successfully.
        :rtype: bool
        """
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
        """
        Generates a token for a given user ID. The function attempts to create a token
        using the user ID. If successful, the newly generated token is logged and
        returned. In case of an error during token generation, the error is logged, and
        None is returned.

        :param user_id: The ID of the user for whom the token is to be generated.
        :type user_id: str
        :return: The generated token if successful, otherwise None.
        :rtype: str or None
        """
        try:
            token = generate_token(user_id)
            self.logger.info(f"Token generated for user {user_id}.")
            return token
        except Exception as e:
            self.logger.error(f"Error generating token for user {user_id}: {e}")
            return None
