from .MusicServer import MusicServer
<<<<<<< HEAD
import asyncio

if __name__ == "__main__":
    # Инициализация Music с параметрами подключения к БД
    
    server = MusicServer(
        host='0.0.0.0', 
        port=1337,
        db_host='localhost',
        db_user='music_user',
        db_password="your_strong_password",
        db_name='music_db',
        db_auth_plugin='mysql_native_password')
=======
from music_db.MusicFileDB import MusicFileDB
import asyncio

if __name__ == "__main__":

    db_host='localhost'
    db_user='music_user'
    db_password=input("Enter the password to connect to the database: ")
    db_name='music_db'
    db_auth_plugin='mysql_native_password'

    musicFile_db = MusicFileDB()

    server = MusicServer(None, musicFile_db, host='0.0.0.0', port=1337)
        
>>>>>>> main
    asyncio.run(server.start())