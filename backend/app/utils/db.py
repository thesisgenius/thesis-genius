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
            from ..models.data import Posts  # , TokenBlacklist
            from ..models.data import (PostComment, Role, SessionLog, Settings,
                                       Thesis, User)

            database_proxy.create_tables(
                [Role, User, Thesis, Posts, PostComment, SessionLog, Settings],
                safe=True,
            )
        app.logger.info("Database initialization complete.")
    except Exception as e:
        app.logger.error(f"Database initialization failed: {e}")
        raise

    return db


# def model_to_dict(model):
#     """
#     Convert a Peewee model instance to a dictionary.
#     """
#     return {field: getattr(model, field) for field in model._meta.sorted_field_names}


def drop_tables(conn_info):
    from peewee import MySQLDatabase

    # Configure the database
    database = MySQLDatabase(
        conn_info["name"],
        user=conn_info["user"],
        password=conn_info["password"],
        host=conn_info["host"],
        port=int(conn_info["port"]),
    )
    database_proxy.initialize(database)

    from ..models.data import (Appendix, Figure, Footnote, PostComment, Posts,
                               Reference, Role, SessionLog, Settings,
                               TableEntry, Thesis, User)

    print("Dropping tables if they exist...")

    # List of models to drop
    models = [
        Settings,
        SessionLog,
        PostComment,
        Posts,
        Reference,
        Thesis,
        User,
        Role,
        Footnote,
        TableEntry,
        Figure,
        Appendix,
    ]

    # Fetch existing table names
    with database_proxy:
        existing_tables = database_proxy.get_tables()

        # Drop only tables that exist
        tables_to_drop = [
            model for model in models if model._meta.table_name in existing_tables
        ]
        if tables_to_drop:
            database_proxy.drop_tables(tables_to_drop, safe=True)
            print(
                f"Dropped tables: {[model._meta.table_name for model in tables_to_drop]}"
            )
        else:
            print("No tables to drop.")


def seed_database(conn_info):
    """
    Seeds the database with initial data for roles, users, theses, references, posts, comments, session logs, and settings.
    """
    from datetime import datetime, timezone

    from peewee import MySQLDatabase

    from ..models.data import (PostComment, Posts, Reference, Role, SessionLog,
                               Settings, Thesis, User)

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
        database_proxy.create_tables(
            [Role, User, Thesis, Reference, Posts, PostComment, SessionLog, Settings],
            safe=True,
        )

    # Seed Roles
    print("Seeding roles...")
    roles = ["Student", "Teacher", "Admin"]
    for role_name in roles:
        if not Role.select().where(Role.name == role_name).exists():
            Role.create(name=role_name)

    # Seed Admin User
    print("Seeding admin user...")
    admin_role = Role.get(Role.name == "Admin")
    if not User.select().where(User.email == "admin@example.com").exists():
        User.create(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            username="admin",
            institution="ThesisGenius University",
            password="securepassword",  # In production, hash this password
            role=admin_role,
            is_admin=True,
        )

    # Seed Student User
    print("Seeding student user...")
    student_role = Role.get(Role.name == "Student")
    student_user = User.get_or_create(
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
    )[0]

    # Seed Thesis
    print("Seeding theses...")
    if not Thesis.select().where(Thesis.title == "Sample Thesis").exists():
        thesis = Thesis.create(
            title="Sample Thesis",
            abstract="This is a sample abstract.",
            content="This is the sample content for the thesis.",
            status="draft",
            student=student_user,
        )

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

    # Seed Posts
    print("Seeding posts...")
    if not Posts.select().where(Posts.title == "Welcome Post").exists():
        post = Posts.create(
            user=student_user,
            title="Welcome Post",
            description="This is the first post in the forum.",
            content="Welcome to the ThesisGenius forum! Feel free to discuss your ideas and share knowledge.",
        )

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
