import os
import subprocess

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from .env
ROOT_USER = os.getenv("LOCAL_ROOT_UN")
ROOT_PW = os.getenv("LOCAL_ROOT_PW")
DB_USER = os.getenv("DEV_DATABASE_USER")
DB_PASSWORD = os.getenv("DEV_DATABASE_PASSWORD")
DB_HOST = os.getenv("DEV_DATABASE_HOST")
DB_NAME = os.getenv("DEV_DATABASE_NAME")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")
SEED_FILE = os.path.join(os.path.dirname(__file__), "seed.sql")  # Optional


def execute_sql_file(db_un, db_pw, sql_file):
    """
    Execute a .sql file against the database.
    """
    try:
        command = f"mysql -u {db_un} -p{db_pw} -h {DB_HOST} {DB_NAME} < {sql_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"Successfully executed {sql_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing {sql_file}: {e}")
        raise


def initialize_database():
    """
    Initializes the database by applying the schema and (optionally) seeding data.
    """
    print("Initializing the database...")
    if os.path.exists(SCHEMA_FILE):
        execute_sql_file(ROOT_USER, ROOT_PW, SCHEMA_FILE)
    else:
        print(f"Schema file not found: {SCHEMA_FILE}")

    # Optional: Load seed data
    if os.path.exists(SEED_FILE):
        execute_sql_file(DB_USER, DB_PASSWORD, SEED_FILE)
    else:
        print(f"Seed file not found: {SEED_FILE}")


if __name__ == "__main__":
    initialize_database()
