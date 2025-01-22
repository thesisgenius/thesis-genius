from datetime import datetime, timezone

from peewee import (AutoField, BooleanField, CharField, DateTimeField,
                    ForeignKeyField, IntegerField, Model, TextField,
                    TimestampField)

from ..utils.db import database_proxy


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Role(BaseModel):
    id = AutoField(primary_key=True, column_name="role_id")
    name = CharField(max_length=20, unique=True, column_name="role_name")

    class Meta:
        table_name = "roles"

    @classmethod
    def validate_role_name(cls, name):
        allowed_roles = {"Student", "Teacher", "Admin"}
        if name not in allowed_roles:
            raise ValueError(
                f"Invalid role name: {name}. Allowed roles are {allowed_roles}."
            )


class User(BaseModel):
    id = AutoField(column_name="user_id", primary_key=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    institution = CharField()
    password = CharField()
    role = ForeignKeyField(
        Role, backref="users", column_name="role_id", on_delete="CASCADE"
    )
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

    def refresh_from_db(self):
        """
        Refresh the model instance with the latest data from the database.
        """
        fresh_instance = User.get(User.id == self.id)
        for field in self._meta.sorted_field_names:
            setattr(self, field, getattr(fresh_instance, field))


class Thesis(BaseModel):
    id = AutoField(primary_key=True, column_name="thesis_id")
    title = CharField()
    course = CharField(null=True)
    instructor = CharField(null=True)
    abstract = TextField(null=True)
    content = TextField(null=True)
    status = CharField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    student = ForeignKeyField(
        User, backref="theses", column_name="student_id", on_delete="CASCADE"
    )

    class Meta:
        table_name = "theses"
        indexes = ((("id", "student_id"), True),)


class Reference(BaseModel):
    id = AutoField(primary_key=True, column_name="reference_id")
    thesis = ForeignKeyField(
        Thesis, backref="references", column_name="thesis_id", on_delete="CASCADE"
    )
    author = CharField()
    title = CharField()
    journal = CharField(null=True)  # Optional for book references
    publication_year = IntegerField(null=True)
    publisher = CharField(null=True)  # Optional
    doi = CharField(null=True)  # Digital Object Identifier (optional)
    created_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "references"
        indexes = ((("id", "thesis_id"), False),)


class Footnote(BaseModel):
    id = AutoField(primary_key=True, column_name="footnote_id")
    thesis = ForeignKeyField(
        Thesis, backref="footnotes", column_name="thesis_id", on_delete="CASCADE"
    )
    content = TextField()

    class Meta:
        table_name = "footnotes"


class TableEntry(BaseModel):
    id = AutoField(primary_key=True, column_name="table_id")
    thesis = ForeignKeyField(
        Thesis, backref="tables", column_name="thesis_id", on_delete="CASCADE"
    )
    caption = CharField(max_length=255)
    file_path = CharField(max_length=255)  # Path to the uploaded file

    class Meta:
        table_name = "tables"


class Figure(BaseModel):
    id = AutoField(primary_key=True, column_name="figure_id")
    thesis = ForeignKeyField(
        Thesis, backref="figures", column_name="thesis_id", on_delete="CASCADE"
    )
    caption = CharField(max_length=255)
    file_path = CharField(max_length=255)  # Path to the uploaded file

    class Meta:
        table_name = "figures"


class Appendix(BaseModel):
    id = AutoField(primary_key=True, column_name="appendix_id")
    thesis = ForeignKeyField(
        Thesis, backref="appendices", column_name="thesis_id", on_delete="CASCADE"
    )
    title = CharField(max_length=255)
    content = TextField(null=True)  # Appendix content
    file_path = CharField(
        max_length=255, null=True
    )  # Optional file upload for the appendix

    class Meta:
        table_name = "appendices"


class Posts(BaseModel):
    id = AutoField()
    user = ForeignKeyField(
        User, backref="posts", column_name="user_id", on_delete="CASCADE"
    )
    title = CharField(max_length=255)
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
    post = ForeignKeyField(Posts, backref="comments")
    content = TextField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "post_comments"
        indexes = ((("id", "user_id"), True),)


class SessionLog(BaseModel):
    id = AutoField(primary_key=True, column_name="session_id")
    user = ForeignKeyField(
        User, backref="sessions", column_name="user_id", on_delete="CASCADE"
    )
    login_time = TimestampField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "session_log"


class Settings(BaseModel):
    id = AutoField(primary_key=True)  # Auto-incrementing primary key
    name = CharField(unique=True, max_length=255)  # Setting name (e.g., 'admin_email')
    value = TextField(null=True)  # Setting value, stored as text

    class Meta:
        table_name = "settings"
