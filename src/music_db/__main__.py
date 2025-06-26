"""Database testing and demonstration script for MusicSQL class."""

from music_db.MusicSQLDB import MusicSQL
import mysql.connector

if __name__ == "__main__":
    """Main execution block for database testing."""

    db_config = {
        'host': 'localhost',
        'user': 'music_user',
        'password': input("Enter the password to connect to the database: "),
        'database': 'music_db',
        'auth_plugin': 'mysql_native_password'
    }


try:
    db = MusicSQL(**db_config)

    # базовая проверка работы
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
    # базовая проверка работы дополнительных фичей
    print("Песни John Doe:")
    for song in db.get_user_songs("john_doe"):
        print(f"- {song[0]} by {song[1]}")

    print("\nПроверка пароля:")
    print("john_doe с правильным паролем:", db.verify_user("john_doe", "qwerty123"))
    print("john_doe с неправильным паролем:", db.verify_user("john_doe", "wrong"))

    print("\nВсе песни:")
    for song in db.get_all_songs():
        print(f"- {song[1]} by {song[2]} (загрузил: {song[0]})")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'db' in locals():
        db.close()
