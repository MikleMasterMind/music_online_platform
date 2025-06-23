from .MusicServer import MusicServer
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
    asyncio.run(server.start())