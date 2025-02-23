from datetime import datetime, timezone

from peewee import (AutoField, BooleanField, CharField, DateTimeField,
                    ForeignKeyField, IntegerField, Model, TextField,
                    TimestampField)

from ..utils.db import database_proxy


class BaseModel(Model):
    class Meta:
        database = database_proxy


class Role(BaseModel):
    """
    Represents a Role within the system.

    The Role model defines roles that can be assigned to users within the system, such
    as "Student", "Teacher", or "Admin". Each role is identified by a unique ID and name.
    The class ensures validity of role names and prevents the creation of invalid roles.

    :ivar id: Auto-generated identifier for the role. It serves as the primary key.
    :type id: AutoField
    :ivar name: Name of the role (e.g., "Student" or "Admin"), which must be unique and is
        constrained to a maximum of 20 characters.
    :type name: CharField
    """

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
    """
    Represents a user entity in the database.

    The class is used to store and manage user-related information such as name, email,
    credentials, and roles. It provides additional utility methods for database
    interaction and model refreshing.

    :ivar id: The unique identifier for a user.
    :type id: AutoField
    :ivar first_name: The first name of the user.
    :type first_name: CharField
    :ivar last_name: The last name of the user.
    :type last_name: CharField
    :ivar email: The email address of the user, must be unique.
    :type email: CharField
    :ivar username: The username of the user, must be unique.
    :type username: CharField
    :ivar institution: The institution of the user.
    :type institution: CharField
    :ivar password: The hashed password of the user.
    :type password: CharField
    :ivar role: The foreign key reference to the Role associated with the user.
    :type role: ForeignKeyField
    :ivar is_admin: A flag indicating whether the user has administrative privileges.
    :type is_admin: BooleanField
    :ivar is_active: A flag indicating whether the user's account is active.
    :type is_active: BooleanField
    :ivar is_authenticated: A flag indicating whether the user is authenticated.
    :type is_authenticated: BooleanField
    :ivar created_at: The timestamp when the user record was created.
    :type created_at: DateTimeField
    :ivar updated_at: The timestamp when the user record was last updated.
    :type updated_at: DateTimeField
    """

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
    profile_picture = CharField(null=True)

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
    """
    Represents a Thesis model used for managing thesis records in a database.

    This model encapsulates data and behavior related to a thesis.
    It stores information such as the title, course, instructor, abstract,
    and content of a thesis, as well as metadata like creation and update
    timestamps. It also maintains a relationship with a student through
    a foreign key field.

    :ivar id: An automatically generated unique identifier for the thesis.
    :type id: AutoField
    :ivar title: The title of the thesis.
    :type title: CharField
    :ivar course: The course associated with the thesis. Can be null.
    :type course: CharField
    :ivar instructor: The instructor supervising the thesis. Can be null.
    :type instructor: CharField
    :ivar abstract: The abstract or summary of the thesis. Can be null.
    :type abstract: TextField
    :ivar content: The full content of the thesis. Can be null.
    :type content: TextField
    :ivar status: The current status of the thesis.
    :type status: CharField
    :ivar created_at: The timestamp when the thesis was created.
    :type created_at: DateTimeField
    :ivar updated_at: The timestamp when the thesis was last updated.
    :type updated_at: DateTimeField
    :ivar student: A reference to the student who authored the thesis.
    :type student: ForeignKeyField

    """

    id = AutoField(primary_key=True, column_name="thesis_id")
    title = CharField()
    course = CharField(null=True)
    instructor = CharField(null=True)
    status = CharField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))
    student = ForeignKeyField(
        User, backref="theses", column_name="student_id", on_delete="CASCADE"
    )

    # Cover Page Fields
    author = CharField(null=True)  # Name of the author
    affiliation = CharField(null=True)  # Institution name
    due_date = DateTimeField(
        null=True, default=datetime.now(timezone.utc)
    )  # Thesis due date

    class Meta:
        table_name = "theses"
        indexes = ((("id", "student_id"), True),)


class TableOfContents(BaseModel):
    """
    Represents a Table of Contents (ToC) entry for a thesis document.

    This class is designed to model the structure of a Table of Contents in relation to
    a thesis. Each instance of the class corresponds to a specific entry in the ToC,
    which includes a section title, the page number, and the order of appearance.
    The entries are unique per thesis and are maintained in a specific order. It
    employs relational mapping to associate ToC entries with their respective thesis.

    :ivar id: Primary key field representing the unique identifier of the
              table of contents entry.
    :type id: AutoField
    :ivar thesis: Foreign key field mapping the ToC entry to a specific thesis.
    :type thesis: ForeignKeyField
    :ivar section_title: Title of the section represented by the ToC entry.
    :type section_title: CharField
    :ivar page_number: Page number where the section begins. Can be null.
    :type page_number: IntegerField
    :ivar order: Order of the section in the ToC. Unique within the context
                 of a single thesis.
    :type order: IntegerField
    """

    id = AutoField(primary_key=True, column_name="toc_id")
    thesis = ForeignKeyField(
        Thesis,
        backref="table_of_contents",
        column_name="thesis_id",
        on_delete="CASCADE",
    )
    section_title = CharField()
    page_number = IntegerField(null=True)
    order = IntegerField()

    class Meta:
        table_name = "thesis_table_of_contents"
        indexes = (
            (("thesis", "order"), True),
        )  # Ensure unique ordering for each thesis


class Abstract(BaseModel):
    """
    Represents the abstract data for a thesis record.

    This class is used to define and interact with the abstract data
    associated with a thesis in the database. It includes the primary key
    for the abstract, the reference to the associated thesis, and a text
    description of the abstract. This model is mapped to the database table
    `thesis_abstracts`.

    :ivar id: The unique identifier for the abstract record.
    :type id: AutoField
    :ivar thesis: The ForeignKey relationship to a thesis. Refers to the
        parent thesis to which this abstract belongs.
    :type thesis: ForeignKeyField
    :ivar text: The text content of the abstract. This may contain the
        summary or details encapsulating the purpose or findings of the
        thesis. It can be null.
    :type text: TextField
    """

    id = AutoField(primary_key=True, column_name="abstract_id")
    thesis = ForeignKeyField(
        Thesis, backref="abstract", column_name="thesis_id", on_delete="CASCADE"
    )
    text = TextField(null=True)

    class Meta:
        table_name = "thesis_abstracts"


class BodyPage(BaseModel):
    """
    Represents a page within the body of a thesis.

    This class is used to define the structure and properties of a thesis body
    page in a database. Each body page is associated with a specific thesis and
    contains information such as the page number and the body content. The class
    is designed to manage and store body pages as part of a thesis management system.

    :ivar id: Unique identifier for the body page.
    :type id: AutoField
    :ivar thesis: Reference to the thesis this body page belongs to.
    :type thesis: ForeignKeyField
    :ivar page_number: The page number within the thesis.
    :type page_number: IntegerField
    :ivar body: The content of the body page.
    :type body: TextField

    """

    id = AutoField(primary_key=True, column_name="body_page_id")
    thesis = ForeignKeyField(
        Thesis, backref="body_pages", column_name="thesis_id", on_delete="CASCADE"
    )
    page_number = IntegerField()
    body = TextField(null=True)

    class Meta:
        table_name = "thesis_body_pages"
        indexes = ((("thesis", "page_number"), True),)


class Reference(BaseModel):
    """
    Represents a Reference entity in the database.

    This class models a reference entry which is related to a thesis. It includes
    details about the reference such as author, title, journal, publication year,
    publisher, and other metadata. It can be used to query or manage reference
    data associated with theses in the system.

    :ivar id: Unique identifier for the reference.
    :type id: AutoField
    :ivar thesis: A foreign key representing the related thesis.
    :type thesis: ForeignKeyField
    :ivar author: The author of the reference.
    :type author: CharField
    :ivar title: The title of the reference.
    :type title: CharField
    :ivar journal: The journal where the reference was published.
                   This is optional for book references.
    :type journal: CharField or None
    :ivar publication_year: The year the reference was published.
    :type publication_year: IntegerField or None
    :ivar publisher: The publisher of the reference.
                     This field is optional.
    :type publisher: CharField or None
    :ivar doi: Digital Object Identifier for the reference.
               This field is optional.
    :type doi: CharField or None
    :ivar created_at: The timestamp when the reference was created.
                      Defaults to the current UTC time.
    :type created_at: DateTimeField

    :meta table_name: references
    :meta indexes: A tuple of indexed fields including `id` and `thesis_id`.
    """

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
    """
    Represents a footnote associated with a thesis.

    This class serves as a model for storing and managing footnotes linked to
    specific theses within the database. Each footnote is uniquely identified
    by an ID and contains textual content along with a reference to its
    associated thesis.

    :ivar id: The unique primary key identifying the footnote.
    :type id: int
    :ivar thesis: The thesis to which this footnote is linked.
    :type thesis: Thesis
    :ivar content: The text content of the footnote.
    :type content: str
    """

    id = AutoField(primary_key=True, column_name="footnote_id")
    thesis = ForeignKeyField(
        Thesis, backref="footnotes", column_name="thesis_id", on_delete="CASCADE"
    )
    content = TextField()

    class Meta:
        table_name = "footnotes"


class TableEntry(BaseModel):
    """
    Represents an entry of a table in the database.

    This class models the structure of a table row within the database. It stores
    details about a table entry including its associated thesis, caption, and the
    file path to the uploaded file. This is primarily used in the context of
    managing and storing tabular data.

    :ivar id: Unique identifier for the table entry.
    :type id: int
    :ivar thesis: Foreign key relation linking to the `Thesis` model. Represents the
        thesis associated with the table entry.
    :type thesis: ForeignKeyField
    :ivar caption: The caption describing the table.
    :type caption: str
    :ivar file_path: Path to the uploaded file associated with the table entry.
    :type file_path: str
    """

    id = AutoField(primary_key=True, column_name="table_id")
    thesis = ForeignKeyField(
        Thesis, backref="tables", column_name="thesis_id", on_delete="CASCADE"
    )
    caption = CharField(max_length=255)
    file_path = CharField(max_length=255)  # Path to the uploaded file

    class Meta:
        table_name = "tables"


class Figure(BaseModel):
    """
    Represents a figure associated with a thesis.

    This class is a database model that defines the structure of the `figures` table. It
    associates a figure with a thesis, stores metadata about the figure, such as a
    caption and its file path, and facilitates interactions with the database. It is
    built using an ORM (Object-Relational Mapping) approach to streamline database
    ops.

    :ivar id: The unique identifier of the figure, serving as the primary key.
    :type id: AutoField
    :ivar thesis: A foreign key reference to the associated Thesis instance.
    :type thesis: ForeignKeyField
    :ivar caption: The caption providing a description of the figure.
    :type caption: CharField
    :ivar file_path: The file path of the uploaded file representing the figure.
    :type file_path: CharField
    """

    id = AutoField(primary_key=True, column_name="figure_id")
    thesis = ForeignKeyField(
        Thesis, backref="figures", column_name="thesis_id", on_delete="CASCADE"
    )
    caption = CharField(max_length=255)
    file_path = CharField(max_length=255)  # Path to the uploaded file

    class Meta:
        table_name = "figures"


class Appendix(BaseModel):
    """
    Represents an Appendix associated with a Thesis.

    This class defines an Appendix model linked to a Thesis. It can be used to store
    additional information, supplementary materials, or any relevant content related
    to a thesis. The Appendix may contain textual content as well as an optional
    file upload for additional resources. The relationship between the Appendix and
    the Thesis is defined as "many-to-one," where many appendices can be linked to
    a single thesis.

    :ivar id: The unique identifier for the appendix.
    :type id: AutoField
    :ivar thesis: The foreign key linking the appendix to a thesis.
    :type thesis: ForeignKeyField
    :ivar title: The title of the appendix.
    :type title: CharField
    :ivar content: The textual content of the appendix. This field is optional.
    :type content: TextField
    :ivar file_path: The file path of an optional uploaded file associated with
        the appendix.
    :type file_path: CharField
    """

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
    """
    Represents posts created by users.

    This class is a model for storing information about posts in a relational
    database. It includes details about the user who created the post, the title,
    description, content, and timestamps for creation and updates. It also maintains
    database-level constraints and indexing to ensure efficient querying and data
    integrity.

    :ivar id: Primary key of the post.
    :type id: AutoField
    :ivar user: Foreign key reference to the User model. Specifies the user who
        created the post. Deletes the post if the associated user is deleted.
    :type user: ForeignKeyField
    :ivar title: Title of the post. Maximum length of 255 characters.
    :type title: CharField
    :ivar description: Optional description of the post.
    :type description: TextField
    :ivar content: The main content of the post.
    :type content: TextField
    :ivar created_at: Timestamp for when the post was created. Defaults to the
        current UTC time.
    :type created_at: DateTimeField
    :ivar updated_at: Timestamp for when the post was last updated. Defaults to the
        current UTC time.
    :type updated_at: DateTimeField
    """

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
    """
    Represents a comment made by a user on a specific post.

    This class handles the structure of user-generated comments on posts.
    Each comment is associated with a user and a post, along with the
    timestamps for when it was created and last updated. This class
    is managed within its defined database table and has pre-defined
    indexing for specific fields.

    :ivar id: An auto-generated unique identifier for the comment.
    :type id: AutoField
    :ivar user: A reference to the user who made the comment.
    :type user: ForeignKeyField
    :ivar post: A reference to the post on which the comment was made.
    :type post: ForeignKeyField
    :ivar content: The text content of the comment.
    :type content: TextField
    :ivar created_at: Timestamp representing when the comment was created.
    :type created_at: DateTimeField
    :ivar updated_at: Timestamp representing the last update time of the comment.
    :type updated_at: DateTimeField
    """

    id = AutoField()
    user = ForeignKeyField(User, backref="comments")
    post = ForeignKeyField(Posts, backref="comments")
    content = TextField()
    created_at = DateTimeField(default=datetime.now(timezone.utc))
    updated_at = DateTimeField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "post_comments"
        indexes = ((("id", "user_id"), True),)

    def get_user_id(self):
        return str(self.user)


class SessionLog(BaseModel):
    """
    Represents a session log entry in the system.

    This class models a session log entry, which links a user to a specific session
    and tracks details such as the user associated with the session and the time
    of login. It is designed to interact with the database, where each entry
    corresponds to a row in the `session_log` table.

    :ivar id: The unique identifier for the session log entry.
    :type id: AutoField
    :ivar user: The user associated with this session.
    :type user: ForeignKeyField
    :ivar login_time: The login timestamp for the session.
    :type login_time: TimestampField
    """

    id = AutoField(primary_key=True, column_name="session_id")
    user = ForeignKeyField(
        User, backref="sessions", column_name="user_id", on_delete="CASCADE"
    )
    login_time = TimestampField(default=datetime.now(timezone.utc))

    class Meta:
        table_name = "session_log"


class Settings(BaseModel):
    """
    Represents the Settings model.

    This class is designed to manage application settings with a unique name and
    a text value. It uses an auto-incrementing primary key for identification.
    This allows dynamic storage and retrieval of various application configuration
    settings.

    :ivar id: Auto-incrementing primary key used to uniquely identify each setting.
    :type id: AutoField
    :ivar name: Unique name for the setting, which acts as an identifier
        (e.g., 'admin_email').
    :type name: CharField
    :ivar value: Value of the setting, stored as text. This can be null.
    :type value: TextField
    """

    id = AutoField(primary_key=True)  # Auto-incrementing primary key
    name = CharField(unique=True, max_length=255)  # Setting name (e.g., 'admin_email')
    value = TextField(null=True)  # Setting value, stored as text

    class Meta:
        table_name = "settings"
