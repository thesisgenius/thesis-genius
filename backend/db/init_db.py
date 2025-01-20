import os

from app.utils.db import drop_tables, seed_database


def initialize_database():
    """
    Initializes the database by applying migrations and seeding initial data.
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
