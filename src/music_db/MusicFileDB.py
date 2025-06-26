"""File storage handler for music files in MP3 format."""

import os


class MusicFileDB:
    """Handles storage and retrieval of music files in a directory.

    Provides methods for:
    - Checking file existence
    - Streaming music files
    - Writing new music files
    - Managing file operations
    """

    def __init__(self, path_to_mp3 = "./music_db/data"):
        """Initialize the music file database with specified directory.

        Args:
            path_to_mp3: Path to directory containing MP3 files.
                        Defaults to './music_db/data'.
        """
        self.path_to_mp3 = path_to_mp3
        if not os.path.exists(path_to_mp3):
            os.makedirs(path_to_mp3)
        files = os.listdir(path_to_mp3)
        mp3_files_only = [f for f in files if os.path.isfile(os.path.join(self.path_to_mp3, f)) and f[len(f) - 3:] == 'mp3']
        self.music_lst = set(mp3_files_only)
        self.opened_file = None

    def music_exist(self, music_title):
        """Check if a music file exists in the database."""
        return music_title in self.music_lst

    def get_music(self, music_title, chunk_size = 4096):
        """Generate that yields chunks of a music file for streaming.

        Args:
            music_title: Name of the music file to stream
            chunk_size: Size of data chunks to yield (default 4096)

        Yields:
            bytes: Chunks of the music file data
            str: File size as first yielded value

        Returns:
            None: If requested file doesn't exist
        """
        if music_title not in self.music_lst:
            return

        filename = f"{self.path_to_mp3}/{music_title}"
        with open(filename, 'rb') as f:
            yield f'{os.path.getsize(filename)}\n'.encode()
            while chunk := f.read(chunk_size):
                yield chunk

    def init_file(self, music_title):
        """Initialize a new music file for writing.

        Args:
            music_title: Name of the new music file (with .mp3 extension)
        """
        filename = f"{self.path_to_mp3}/{music_title}"
        self.opened_file = open(filename, 'wb')
        self.music_lst.add(music_title)

    def write_data(self, data):
        """Write data to the currently open music file.

        Args:
            data: Data to write to the file
        """
        if self.opened_file:
            self.opened_file.write(data)

    def close_file(self):
        """Close the currently open music file."""
        self.opened_file = None
