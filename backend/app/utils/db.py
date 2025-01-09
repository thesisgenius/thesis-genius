from peewee import MySQLDatabase, Proxy, SqliteDatabase

# Create a database proxy to allow initialization later
database_proxy = Proxy()


def initialize_database(app):
    """
    Initialize the correct database based on the provided Flask app configuration.
    """
    conn_info = app.config["DB_CONNECTION_INFO"]

    try:
        if conn_info["engine"] == "mysql":
            db = MySQLDatabase(
                conn_info["name"],
                user=conn_info["user"],
                password=conn_info["password"],
                host=conn_info["host"],
                port=int(conn_info["port"]),
            )
        elif conn_info["engine"] == "sqlite":
            db = SqliteDatabase(conn_info["name"])
        else:
            raise ValueError(f"Unsupported database engine: {conn_info['engine']}")

        # Bind the database proxy
        database_proxy.initialize(db)

        # Connect to the database and create tables
        app.logger.info("Connecting to the database...")
        with database_proxy:
            from ..models.data import Post, PostComment, Settings, Thesis, User

            database_proxy.create_tables(
                [User, Thesis, Post, Settings, PostComment], safe=True
            )
        app.logger.info("Database initialization complete.")
    except Exception as e:
        app.logger.error(f"Database initialization failed: {e}")
        raise

    return db


def model_to_dict(model):
    """
    Convert a Peewee model instance to a dictionary.
    """
    return {field: getattr(model, field) for field in model._meta.sorted_field_names}
