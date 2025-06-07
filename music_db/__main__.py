from Music import Music
from mysql.connector import Error
import mysql.connector

if __name__ == "__main__":
    db_config = {
        'host': 'localhost',
        'user': 'music_user',
        'password': input("Enter the password to connect to the database: "),
        'database': 'music_db',
        'auth_plugin': 'mysql_native_password'
    }
    
    
try:
    db = Music(**db_config)

    #базовая проверка работы
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM songs WHERE nickname IN ('john_doe', 'jane_smith')")
    cursor.execute("DELETE FROM users WHERE nickname IN ('john_doe', 'jane_smith')")
    db.connection.commit()
    cursor.close()

    db.add_user("john_doe", "John Doe", "qwerty123")
    db.add_user("jane_smith", "Jane Smith", "password123")

    db.add_song("john_doe", "Bohemian Rhapsody", "Queen")
    db.add_song("john_doe", "Stairway to Heaven", "Led Zeppelin")
    db.add_song("jane_smith", "Imagine", "John Lennon")

    print("Data added successfully!")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
        if 'db' in locals():
            db.close()