import click
from db.init_db import initialize_database


@click.group()
def db_cli():
    """
    Defines the `db_cli` group function, which serves as the entry point for a
    Click-based command-line interface (CLI) group related to database operations.

    This function uses the Click framework to handle grouping of multiple CLI
    commands under a common namespace called `db_cli`. The grouped commands
    can be invoked as subcommands to this main group.

    :return: A Click CLI group instance that can be used to register subcommands.
    :rtype: click.Group
    """
    pass


@db_cli.command()
def init():
    """
    Initializes the database and displays a success message.

    This function performs the initialization of the application's database,
    setting it up for use. After initialization, a confirmation message is
    displayed to the user.

    :return: None
    """
    initialize_database()
    click.echo("Database initialized successfully.")
