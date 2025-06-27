"""Main entry point for the music server application."""
from .MusicServer import MusicServer
from src.music_db.MusicFileDB import MusicFileDB
import asyncio


def start():
    """Initialize and run the music server with specified configuration."""
    musicFile_db = MusicFileDB()

    server = MusicServer(None, musicFile_db, host='0.0.0.0', port=1337)

    asyncio.run(server.start())


if __name__ == "__main__":
    start()
