from mysql.connector import Error

from server import logger


class DBManager:
    def __init__(self, host="localhost", root_user="root", root_password=""):
        """
        Initialize the DBManager with connection details for the MySQL server.
        :param host: The MySQL server host (default: localhost).
        :param root_user: The root username (default: root).
        :param root_password: The root password.
        """
        self.host = host
        self.root_user = root_user
        self.root_password = root_password
        self.connection = None

    def connect(self):
        """
        Establish a connection to the MySQL server using root credentials.
        """
        try:
            import pymysql
            self.connection = pymysql.connect(
                host=self.host,
                user=self.root_user,
                password=self.root_password
            )
            logger.info("Successfully connected to MySQL server using pymysql.")
        except Exception as e:
            logger.error(f"Error connecting to MySQL server: {e}")
            self.connection = None


    def create_database(self, database_name):
        """
        Create a new database.
        :param database_name: Name of the database to create.
        """
        if not self.connection:
            logger.info("No active connection. Call connect() first.")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
            logger.info(f"Database '{database_name}' created successfully.")
        except Error as e:
            logger.error(f"Error creating database '{database_name}': {e}")
            return

    def create_user(
        self, username, password, database_table, privileges="ALL PRIVILEGES", host="localhost"
    ):
        """
        Create a new MySQL user and grant privileges.
        :param username: The username of the new user.
        :param password: The password for the new user.
        :param privileges: Privileges to grant (default: ALL PRIVILEGES).
        :param host: The host for the user (default: localhost).
        :param database_table: The database table to grant privileges on (default: {database_table}.*).
        """
        if not self.connection:
            logger.info("No active connection. Call connect() first.")
            return

        try:
            cursor = self.connection.cursor()
            # Create the user
            cursor.execute(
                f"CREATE USER IF NOT EXISTS '{username}'@'{host}' IDENTIFIED BY '{password}';"
            )
            logger.info(f"User '{username}'@'{host}' created successfully.")

            # Grant privileges
            cursor.execute(f"GRANT {privileges} ON {database_table}.* TO '{username}'@'{host}';")
            logger.info(f"Privileges '{privileges}' granted to '{username}'@'{host}'.")

            # Flush privileges
            cursor.execute("FLUSH PRIVILEGES;")
            logger.info("Privileges flushed successfully.")
        except Error as e:
            logger.error(f"Error creating user '{username}'@'{host}': {e}")

    def execute_sql_file(self, sql_file_path):
        """
        Execute an SQL file on the MySQL server using pymysql.
        :param sql_file_path: Path to the SQL file to execute.
        """
        logger.info(f"Executing SQL file: {sql_file_path}")
        if not self.connection:
            logger.info("No active connection. Call connect() first.")
            return

        try:
            cursor = self.connection.cursor()
            with open(sql_file_path, "r") as sql_file:
                sql_script = sql_file.read()

                # Split the SQL file into commands
                sql_commands = sql_script.split(";")
                for idx, command in enumerate(sql_commands):
                    command = command.strip()  # Clean up whitespace
                    if command:  # Ignore empty commands
                        logger.debug(f"Executing SQL command {idx + 1}: {command}")
                        cursor.execute(command)

                self.connection.commit()  # Commit changes after all commands
                logger.info(f"SQL file '{sql_file_path}' executed successfully.")
        except Exception as e:
            logger.error(f"Error executing SQL file '{sql_file_path}': {e}")
            self.connection.rollback()  # Rollback on error
        finally:
            cursor.close()


    def close_connection(self):
        """
        Close the connection to the MySQL server.
        """
        if self.connection:
            self.connection.close()
            logger.info("Connection to MySQL server closed.")
        else:
            logger.warn("No active connection to close.")
