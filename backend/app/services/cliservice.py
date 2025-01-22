# services/cliservice.py
from backend.db.init_db import initialize_database

from ..utils.db import migrate_database, seed_database


class CLIService:
    @staticmethod
    def initialize_db():
        initialize_database()

    @staticmethod
    def migrate():
        migrate_database()

    @staticmethod
    def seed():
        seed_database()
