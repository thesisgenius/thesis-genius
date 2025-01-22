import click
from app.utils.db import seed_database
from db.init_db import initialize_database


@click.group()
def db_cli():
    """Database management commands."""
    pass


@db_cli.command()
def init():
    """Initialize the database (migrate and seed)."""
    initialize_database()
    click.echo("Database initialized successfully.")


@db_cli.command()
def seed():
    """Seed the database with initial data."""
    seed_database()
    click.echo("Database seeded successfully.")
