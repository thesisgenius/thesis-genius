import click
from app.models.data import Role, User
from peewee import DoesNotExist


@click.group()
def user_cli():
    """User management commands."""
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
    """Create a new user."""
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
    """Delete a user by email."""
    try:
        user = User.get(User.email == email)
        user.delete_instance()
        click.echo(f"User '{email}' deleted successfully.")
    except DoesNotExist:
        click.echo(f"Error: User with email '{email}' does not exist.")


@user_cli.command()
@click.option("--role", help="Filter users by role.")
def list(role):
    """List all users, optionally filtered by role."""
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
    """Update a user's details by email."""
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
