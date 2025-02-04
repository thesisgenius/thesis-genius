import os

import click
from app import create_app  # Use absolute import for Flask app
from cli.db import db_cli
from cli.user import user_cli
from dotenv import load_dotenv

# Load environment variables for the CLI
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


@click.group()
def cli():
    """
    This function serves as the entry point for a Click command-line interface (CLI) application. It defines a group of
    commands to which individual CLI commands can be added. This group enables logical organization and handling
    of multiple commands within a single CLI application.

    :return: None
    """
    pass


# Add subcommands for database and user management
cli.add_command(db_cli, name="db")
cli.add_command(user_cli, name="user")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host for the Flask application.")
@click.option("--port", default=8557, help="Port for the Flask application.")
@click.option("--env", default="development", help="Runtime environment for Flask.")
def run(host, port, env):
    """
    Runs a Flask application server.

    This function sets up and starts a Flask application server based on the provided
    host, port, and runtime environment. It logs the startup information and raises an
    exception in case of a failure during execution.

    :param host: The hostname or IP address where the Flask application will run.
    :param port: The port number on which the Flask server will listen.
    :param env: The Flask runtime environment (e.g., "development", "production").
    :return: None
    """
    try:
        app = create_app(env)
        app.logger.info(f"Starting Flask server in {env} environment")
        app.run(host=host, port=port)
    except Exception as e:
        click.echo(f"Failed to start the application: {e}")
        raise


if __name__ == "__main__":
    cli()
