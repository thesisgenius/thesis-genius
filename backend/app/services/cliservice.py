from backend.db.init_db import initialize_database


class CLIService:
    """
    Provides command-line interface services for managing and interacting with
    the application, such as database initialization and other operations.

    This class encapsulates static methods aimed at streamlining
    specific administrative tasks. It serves as a utility for
    developers or administrators to perform tasks without
    requiring extensive manual intervention or additional scripts.
    """

    @staticmethod
    def initialize_db():
        initialize_database()
