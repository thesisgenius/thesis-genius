import os

from app.utils.db import drop_tables, seed_database


def initialize_database():
    """
    Initializes the development database by dropping all existing tables and reseeding
    it with initial data. This function retrieves database connection information from
    environment variables and applies required migrations to prepare the database for
    development use. If the relevant environment variables are not found, default
    values are used instead.

    :raises KeyError: If critical environment variables are missing and not provided
        in function defaults.
    :raises ConnectionError: If a connection to the database using the provided
        credentials cannot be established.
    :raises RuntimeError: If any issue occurs during seeding or migration of the
        database.

    :return: None
    """
    print("Initializing database...")
    conn_info = {
        "name": os.getenv("DEV_DATABASE_NAME", "thesis_app_dev"),
        "engine": os.getenv("DEV_DATABASE_ENGINE", "mysql"),
        "user": os.getenv("DEV_DATABASE_USER", "thesis_dev"),
        "password": os.getenv("DEV_DATABASE_PASSWORD", "dev_password"),
        "host": os.getenv("DEV_DATABASE_HOST", "localhost"),
        "port": 3306,
    }
    drop_tables(conn_info)  # Apply migrations
    print("Dropped all table data successfully.")

    print("Seeding the database...")
    seed_database(conn_info)  # Seed initial data
    print("Database seeded successfully.")
