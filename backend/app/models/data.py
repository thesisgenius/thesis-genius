from datetime import datetime, timezone

from flask import current_app as app
from peewee import (AutoField, BooleanField, CharField, DatabaseProxy,
                    DateTimeField, ForeignKeyField, Model, MySQLDatabase,
                    SqliteDatabase, TextField)

# Proxy for lazy initialization
database_proxy = DatabaseProxy()

def initialize_database(config):
    """
    Initialize the correct database based on the provided configuration.
    """
    conn_info = config["DB_CONNECTION_INFO"]

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

    return db


class BaseModel(Model):
    class Meta:
        database = database_proxy


class User(BaseModel):
    id = AutoField()
    name = CharField()
    email = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_authenticated = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "users"
        indexes = ((("id", "email"), True),)

    def get_id(self):
        return str(self.id)

class Theses(BaseModel):
    id = AutoField()
    title = CharField()
    abstract = TextField()
    status = CharField()
    submission_date = DateTimeField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    user = ForeignKeyField(User, backref="theses")

    class Meta:
        table_name = "theses"
        indexes = ((("id", "user_id"), True),)


class Post(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="posts")
    title = CharField()
    description = TextField(null=True)
    content = TextField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "posts"
        indexes = ((("id", "user_id"), True),)


class PostComment(BaseModel):
    id = AutoField()
    user = ForeignKeyField(User, backref="comments")
    post = ForeignKeyField(Post, backref="comments")
    content = TextField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "post_comments"
        indexes = ((("id", "user_id"), True),)


class Settings(BaseModel):
    id = AutoField(primary_key=True)  # Auto-incrementing primary key
    name = CharField(unique=True, max_length=255)  # Setting name (e.g., 'admin_email')
    value = TextField(null=True)  # Setting value, stored as text

    class Meta:
        table_name = "settings"
