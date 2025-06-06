import mysql.connector
from mysql.connector import Error
from typing import List, Tuple, Optional

class Music:
    def __init__(self, host: str, user: str, password: str, database: str, auth_plugin: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.auth_plugin = auth_plugin
        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Establishes a connection with MySQL"""
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
        """Creates the users and songs tables if they do not exist"""
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
        """Adds a new user"""
        try:
            cursor = self.connection.cursor()
            #cursor.execute(
            #"INSERT IGNORE INTO users (nickname, username, password) VALUES (%s, %s, %s)",
            #(nickname, username, password)
        #)
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
        """Adds a new song"""
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
        """Closes the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()