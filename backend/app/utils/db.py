import inspect

from peewee import MySQLDatabase, Proxy, SqliteDatabase

# Create a database proxy to allow initialization later
database_proxy = Proxy()


def initialize_database(app):
    """
    Initializes the application's database connection and schema.

    This function configures the database connection based on the application's
    configuration and prepares the database by dynamically detecting and
    synchronizing all models from the `data` module.

    :param app: The Flask application instance containing configuration settings.
    :type app: Flask

    :return: Initialized database object prepared for use.
    :rtype: peewee.Database
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
            # Dynamically detect all models in data.py and sync tables
            from peewee import CharField, DateTimeField, Model
            from playhouse.migrate import (MySQLMigrator, SqliteMigrator,
                                           migrate)

            from ..models import data

            database_models = [
                cls
                for _, cls in inspect.getmembers(
                    data,
                    lambda m: isinstance(m, type)
                    and issubclass(m, Model)
                    and m != Model,
                )
            ]
            app.logger.info(
                f"Found {len(database_models)} models to sync: {[model.__name__ for model in database_models]}"
            )
            # Ensure tables exist
            database_proxy.create_tables(database_models, safe=True)

            # Perform schema migrations if necessary
            app.logger.info("Checking for missing columns...")
            migrator = (
                MySQLMigrator(db)
                if conn_info["engine"] == "mysql"
                else SqliteMigrator(db)
            )

            # Check for missing columns in the Thesis table
            with database_proxy:
                existing_columns = db.get_columns("theses")
                existing_column_names = {col.name for col in existing_columns}

                migrations = []
                if "author" not in existing_column_names:
                    app.logger.info("Adding missing column: author")
                    migrations.append(
                        migrator.add_column("theses", "author", CharField(null=True))
                    )

                if "affiliation" not in existing_column_names:
                    app.logger.info("Adding missing column: affiliation")
                    migrations.append(
                        migrator.add_column(
                            "theses", "affiliation", CharField(null=True)
                        )
                    )

                if "due_date" not in existing_column_names:
                    app.logger.info("Adding missing column: due_date")
                    migrations.append(
                        migrator.add_column(
                            "theses", "due_date", DateTimeField(null=True)
                        )
                    )

                if "degree" not in existing_column_names:
                    app.logger.info("Adding missing column: degree")
                    migrations.append(
                        migrator.add_column("theses", "degree", CharField(null=True))
                    )

                existing_columns_signature = db.get_columns("signature_pages")
                existing_columns_signature_name = {
                    col.name for col in existing_columns_signature
                }

                if "chair" not in existing_columns_signature_name:
                    app.logger.info("Adding missing column: chair")
                    migrations.append(
                        migrator.add_column(
                            "signature_pages", "chair", CharField(null=True)
                        )
                    )

                if migrations:
                    migrate(*migrations)
                    app.logger.info("Schema migration completed successfully.")
                else:
                    app.logger.info("No schema changes detected.")

        app.logger.info("Database initialization complete.")
    except Exception as e:
        app.logger.error(f"Database initialization failed: {e}")
        raise

    return db


def drop_tables(conn_info):
    """
    Drops existing database tables dynamically by retrieving model definitions
    from the provided module and comparing them with existing tables in the
    database. Only tables that match existing definitions are dropped to prevent
    errors.

    :param conn_info: A dictionary containing database connection details. The
        keys in the dictionary are expected to include "name" (database name),
        "user" (database username), "password" (database password), "host"
        (database host), and "port" (port number for the database connection).
    :type conn_info: dict
    :return: None
    :rtype: NoneType
    """
    from peewee import MySQLDatabase

    from ..models import data

    # Configure the database
    database = MySQLDatabase(
        conn_info["name"],
        user=conn_info["user"],
        password=conn_info["password"],
        host=conn_info["host"],
        port=int(conn_info["port"]),
    )
    database_proxy.initialize(database)

    print("Dropping tables if they exist...")

    # Dynamically retrieve all models from data.py
    database_models = [
        model
        for model in data.__dict__.values()
        if isinstance(model, type)
        and issubclass(model, data.BaseModel)
        and model is not data.BaseModel
    ]

    # Fetch existing table names
    with database_proxy:
        existing_tables = database_proxy.get_tables()

        # Drop only tables that exist
        tables_to_drop = [
            model
            for model in database_models
            if model._meta.table_name in existing_tables
        ]
        if tables_to_drop:
            database_proxy.drop_tables(tables_to_drop, safe=True)
            print(f"Dropped tables: {[model.__name__ for model in tables_to_drop]}")
        else:
            print("No tables to drop.")


def seed_database(conn_info):
    """
    Seeds the database with initial data, ensuring all necessary tables and default
    entries are created. The function sets up user roles, default users, thesis
    data, references, figures, tables, and other necessary entries to prepare the
    application for use.

    .. note::
        Sensitive data like passwords in this function should follow secure
        practices such as using password hashing in a production environment.

    :param conn_info: Contains the database connection information.
                      Expected keys are "name", "user", "password", "host", "port".
                      Use them to establish the connection with the database.
    :type conn_info: dict[str, str | int]
    :return: None
    """
    from datetime import datetime, timezone

    from peewee import MySQLDatabase

    from ..models.data import (Appendix, Figure, Footnote, PostComment, Posts,
                               Reference, Role, SessionLog, Settings,
                               TableEntry, Thesis, User)

    # Configure the database
    database = MySQLDatabase(
        conn_info["name"],
        user=conn_info["user"],
        password=conn_info["password"],
        host=conn_info["host"],
        port=int(conn_info["port"]),
    )
    database_proxy.initialize(database)

    # Ensure tables exist
    print("Ensuring all tables exist...")
    with database_proxy:
        # Dynamically detect all models in data.py and sync tables
        from peewee import Model

        from ..models import data

        database_models = [
            cls
            for _, cls in inspect.getmembers(
                data,
                lambda m: isinstance(m, type) and issubclass(m, Model) and m != Model,
            )
        ]
        database_proxy.create_tables(database_models, safe=True)

    # Seed Roles
    print("Seeding roles...")
    roles = ["Student", "Teacher", "Admin"]
    for role_name in roles:
        Role.get_or_create(name=role_name)

    # Seed Admin User
    print("Seeding admin user...")
    admin_role = Role.get(Role.name == "Admin")
    User.get_or_create(
        email="admin@example.com",
        defaults={
            "first_name": "Admin",
            "last_name": "User",
            "username": "admin",
            "institution": "ThesisGenius University",
            "password": "securepassword",  # In production, hash this password
            "role": admin_role,
            "is_admin": True,
        },
    )

    # Seed Student User
    print("Seeding student user...")
    student_role = Role.get(Role.name == "Student")
    student_user, _ = User.get_or_create(
        email="student@example.com",
        defaults={
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "institution": "ThesisGenius University",
            "password": "studentpassword",  # In production, hash this password
            "role": student_role,
            "is_admin": False,
        },
    )

    # Seed Thesis
    print("Seeding theses...")
    thesis, created = Thesis.get_or_create(
        title="Sample Thesis",
        defaults={
            "abstract": "This is a sample abstract.",
            "content": "This is the sample content for the thesis.",
            "status": "draft",
            "student": student_user,
        },
    )

    if created:
        # Seed References
        print("Seeding references...")
        Reference.create(
            thesis=thesis,
            author="John Smith",
            title="Artificial Intelligence in Education",
            journal="AI Journal",
            publication_year=2022,
            doi="10.1234/aij.2022.001",
        )
        Reference.create(
            thesis=thesis,
            author="Jane Doe",
            title="Machine Learning Applications",
            publisher="Future Publishing",
            publication_year=2023,
        )

        # Seed Footnotes
        print("Seeding footnotes...")
        Footnote.create(
            thesis=thesis,
            content="This is a sample footnote.",
            page_number=1,
        )

        # Seed Tables
        print("Seeding tables...")
        TableEntry.create(
            thesis=thesis,
            title="Sample Table",
            description="This is a sample table description.",
            data="Column1,Column2\nData1,Data2",
        )

        # Seed Figures
        print("Seeding figures...")
        Figure.create(
            thesis=thesis,
            title="Sample Figure",
            description="This is a sample figure description.",
            image_url="https://example.com/sample-figure.jpg",
        )

        # Seed Appendices
        print("Seeding appendices...")
        Appendix.create(
            thesis=thesis,
            title="Sample Appendix",
            content="This is a sample appendix content.",
        )

    # Seed Posts
    print("Seeding posts...")
    post, created = Posts.get_or_create(
        title="Welcome Post",
        defaults={
            "user": student_user,
            "description": "This is the first post in the forum.",
            "content": "Welcome to the ThesisGenius forum! Feel free to discuss your ideas and share knowledge.",
        },
    )

    if created:
        # Seed Comments
        print("Seeding post comments...")
        PostComment.create(
            user=student_user,
            post=post,
            content="This is a comment on the welcome post.",
        )

    # Seed Settings
    print("Seeding settings...")
    settings = [
        {"name": "site_name", "value": "ThesisGenius"},
        {"name": "admin_email", "value": "admin@example.com"},
    ]
    for setting in settings:
        Settings.get_or_create(
            name=setting["name"], defaults={"value": setting["value"]}
        )

    # Seed Session Logs
    print("Seeding session logs...")
    if not SessionLog.select().where(SessionLog.user == student_user).exists():
        SessionLog.create(
            user=student_user,
            login_time=datetime(2023, 12, 25, 10, 30, tzinfo=timezone.utc),
        )
        SessionLog.create(
            user=student_user,
            login_time=datetime(2024, 1, 1, 15, 45, tzinfo=timezone.utc),
        )

    print("Database seeding complete!")
