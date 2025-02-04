import click
from app.models.data import Role, User
from peewee import DoesNotExist


@click.group()
def user_cli():
    """
    A command-line interface (CLI) group for handling user-related commands.

    This CLI group serves as an entry point for managing various operations
    related to users. It acts as a container for multiple commands that can be
    defined and executed to process user-related tasks. Each command within this
    group can perform a specific operation.

    :return: Returns the `click.Group` instance initialized for the user CLI.
    :rtype: click.Group
    """
    pass


@user_cli.command()
@click.argument("email")
@click.argument("password")
@click.option("--role", default="Student", help="Role for the user (default: Student).")
@click.option("--first-name", default="Default", help="First name of the user.")
@click.option("--last-name", default="User", help="Last name of the user.")
@click.option(
    "--institution", default="ThesisGenius University", help="User's institution."
)
def create(email, password, role, first_name, last_name, institution):
    """
    This function is a command-line utility for creating a new user in the system. It allows
    the addition of a user with specified attributes such as email, password, role, first
    name, last name, and institution. The function validates the provided role to ensure
    it exists and checks if the given email is already associated with an existing user.
    If both checks pass, a new user is created, and the operation result is printed to the
    console.

    :param email: Email address of the user to be created. This will also serve as a part of the username.
    :param password: Password for the user. In production, this should be securely hashed.
    :param role: Role assigned to the user (default is "Student").
    :param first_name: First name of the user (default is "Default").
    :param last_name: Last name of the user (default is "User").
    :param institution: Institution associated with the user (default is "ThesisGenius University").
    :return: None. Outputs a success or error message to the console.
    """
    try:
        # Fetch the role object
        role_obj = Role.get(Role.name == role)
    except DoesNotExist:
        click.echo(f"Error: Role '{role}' does not exist.")
        return

    if User.select().where(User.email == email).exists():
        click.echo(f"Error: A user with email '{email}' already exists.")
        return

    # Create the user
    user = User.create(
        email=email,
        password=password,  # In production, hash this password
        first_name=first_name,
        last_name=last_name,
        username=email.split("@")[0],  # Default username from email
        institution=institution,
        role=role_obj,
        is_admin=(role == "Admin"),
    )
    click.echo(f"User '{user.email}' created successfully with role '{role}'.")


@user_cli.command()
@click.argument("email")
def delete(email):
    """
    Delete a user from the database based on their email. This method retrieves a user
    using the provided email and removes the corresponding record from the database.
    If the user does not exist, it displays an appropriate error message.

    :param email: The email of the user to delete
    :type email: str
    :return: None
    """
    try:
        user = User.get(User.email == email)
        user.delete_instance()
        click.echo(f"User '{email}' deleted successfully.")
    except DoesNotExist:
        click.echo(f"Error: User with email '{email}' does not exist.")


@user_cli.command()
@click.option("--role", help="Filter users by role.")
def list(role):
    """
    Lists users optionally filtered by a specified role.

    The function retrieves and displays a list of users from the database. If a role
    is specified, it filters the users by the specified role. If the role does not
    exist in the database, an error message is displayed. If no users are found,
    a message indicating this is shown.

    :param role: Filters the list of users to show only users with the specified
        role. If not specified, all users are listed.
    :type role: str or None

    :return: None
    """
    if role:
        try:
            role_obj = Role.get(Role.name == role)
            users = User.select().where(User.role == role_obj)
        except DoesNotExist:
            click.echo(f"Error: Role '{role}' does not exist.")
            return
    else:
        users = User.select()

    if users:
        click.echo("Users:")
        for user in users:
            click.echo(f" - {user.email} ({user.role.name})")
    else:
        click.echo("No users found.")


@user_cli.command()
@click.argument("email")
@click.option("--password", help="Update the user's password.")
@click.option("--first-name", help="Update the user's first name.")
@click.option("--last-name", help="Update the user's last name.")
@click.option("--role", help="Update the user's role.")
@click.option("--institution", help="Update the user's institution.")
def update(email, password, first_name, last_name, role, institution):
    """
    Updates the properties of an existing user in the system. Allows updating the
    user's password, first name, last name, role, and institution by providing
    appropriate options. Throws an error if the user or role does not exist.

    :param email: Email of the user to be updated
    :type email: str
    :param password: New password for the user
    :type password: Optional[str]
    :param first_name: New first name of the user
    :type first_name: Optional[str]
    :param last_name: New last name of the user
    :type last_name: Optional[str]
    :param role: New role of the user
    :type role: Optional[str]
    :param institution: New institution of the user
    :type institution: Optional[str]
    :return: None
    :rtype: None
    """
    try:
        user = User.get(User.email == email)
        if password:
            user.password = password  # In production, hash this password
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if role:
            try:
                role_obj = Role.get(Role.name == role)
                user.role = role_obj
                user.is_admin = role == "Admin"
            except DoesNotExist:
                click.echo(f"Error: Role '{role}' does not exist.")
                return
        if institution:
            user.institution = institution

        user.save()
        click.echo(f"User '{email}' updated successfully.")
    except DoesNotExist:
        click.echo(f"Error: User with email '{email}' does not exist.")
