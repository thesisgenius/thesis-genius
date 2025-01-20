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
    """ThesisGenius CLI - Manage backend operations."""
    pass


# Add subcommands for database and user management
cli.add_command(db_cli, name="db")
cli.add_command(user_cli, name="user")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host for the Flask application.")
@click.option("--port", default=8557, help="Port for the Flask application.")
@click.option("--env", default="development", help="Runtime environment for Flask.")
def run(host, port, env):
    """Run the Flask application."""
    try:
        app = create_app(env)
        app.logger.info(f"Starting Flask server in {env} environment")
        app.run(host=host, port=port)
    except Exception as e:
        click.echo(f"Failed to start the application: {e}")
        raise


if __name__ == "__main__":
    cli()
