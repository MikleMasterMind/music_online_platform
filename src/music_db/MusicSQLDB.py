"""Database handler for music application using MySQL."""

import mysql.connector
from mysql.connector import Error
from typing import List, Tuple


class MusicSQLDB:
    """Handles all database operations for the music application.

    Manages connections to MySQL database and provides methods for:
    - User registration and authentication
    - Song management
    - Data retrieval
    """

    def __init__(self, host: str, user: str, password: str, database: str, auth_plugin: str):
        """Initialize database connection and setup required tables.

        Args:
            host: MySQL server host address
            user: Database username
            password: Database password
            database: Name of the database to connect to
            auth_plugin: Authentication plugin to use
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.auth_plugin = auth_plugin
        self.connection = None
        self.registered_users: set = set()
        self._connect()
        self._create_tables()

    def _connect(self):
        """Establish a connection with MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise

    def _create_tables(self):
        """Create the users and songs tables if they do not exist."""
        try:
            cursor = self.connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    nickname VARCHAR(50) PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    song_id INT AUTO_INCREMENT PRIMARY KEY,
                    nickname VARCHAR(50),
                    song_name VARCHAR(100) NOT NULL,
                    author VARCHAR(100) NOT NULL,
                    FOREIGN KEY (nickname) REFERENCES users(nickname)
                    ON DELETE CASCADE
                )
            """)

            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error when creating tables: {e}")
            raise

    def add_user(self, nickname: str, username: str, password: str) -> bool:
        """Add a new user."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (nickname, username, password) VALUES (%s, %s, %s)",
                (nickname, username, password)
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error when adding a user: {e}")
            return False

    def add_song(self, nickname: str, song_name: str, author: str) -> bool:
        """Add a new song."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO songs (nickname, song_name, author) VALUES (%s, %s, %s)",
                (nickname, song_name, author)
            )
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error when adding a song: {e}")
            return False

    def close(self):
        """Close the database connection if it's open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def get_user_songs(self, nickname: str) -> List[Tuple]:
        """Retrieve all songs belonging to a specific user."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT song_name, author FROM songs WHERE nickname = %s",
                (nickname,)
            )
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error when receiving user's songs: {e}")
            return []

    def get_all_songs(self) -> List[Tuple]:
        """Retrieve all songs in the database with user information."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT u.username, s.song_name, s.author
                FROM songs s
                JOIN users u ON s.nickname = u.nickname
            """)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error when receiving all songs: {e}")
            return []

    def verify_user(self, nickname: str, password: str) -> bool:
        """Verify if provided credentials match a user in database."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT password FROM users WHERE nickname = %s",
                (nickname,)
            )
            result = cursor.fetchone()
            cursor.close()
            return result is not None and result[0] == password
        except Error as e:
            print(f"Error when verifying the user: {e}")
            return False

    def get_registered_users(self) -> set:
        """Get set of all registered user nicknames."""
        return self.registered_users

    def update_registered_users(self) -> None:
        """Update internal set of registered users from database."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT nickname FROM users")
                result = cursor.fetchall()
                self.registered_users = {row[0] for row in result} if result else set()
        except Error as e:
            print(f"Error when getting all regisrtered users: {e}")
