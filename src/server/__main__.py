from .MusicServer import MusicServer
from music_db.MusicFileDB import MusicFileDB
import asyncio

if __name__ == "__main__":

    db_host='localhost'
    db_user='music_user'
    db_password=""
    db_name='music_db'
    db_auth_plugin='mysql_native_password'

    musicFile_db = MusicFileDB()

    server = MusicServer(None, musicFile_db, host='0.0.0.0', port=1337)
        
    asyncio.run(server.start())