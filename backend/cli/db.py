import os

import click
from app.utils.db import migrate_database, seed_database
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
def migrate():
    """Run database migrations."""
    migrate_database(
        {
            "name": os.getenv("DEV_DATABASE_NAME", "thesis_app_dev"),
            "engine": os.getenv("DEV_DATABASE_ENGINE", "mysql"),
            "user": os.getenv("DEV_DATABASE_USER", "thesis_dev"),
            "password": os.getenv("DEV_DATABASE_PASSWORD", "dev_password"),
            "host": os.getenv("DEV_DATABASE_HOST", "localhost"),
            "port": 3306,
        }
    )
    click.echo("Migrations applied successfully.")


@db_cli.command()
def seed():
    """Seed the database with initial data."""
    seed_database()
    click.echo("Database seeded successfully.")
