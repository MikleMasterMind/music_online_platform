"""Command processor for handling music server operations and file management."""


class ConectProcessor:
    """Processes client commands and manages interactions."""

    def __init__(self, musicSQL_db, musicFile_db, logged_users):
        """Init the ConectProcessor with connections music file.

        Args:
            musicSQL_db: Database connection for music metadata
            musicFile_db: File storage system for music files
        """
        self.musicSQL = musicSQL_db
        self.musicFile = musicFile_db

    async def process_command(self, command, writer) -> list:
        """Process incoming client commands and return appropriate responses.

        Args:
            command: List of command components from client input
            writer: StreamWriter object for the client connection

        Returns:
            list: Response package containing either:
                - ["TEXT", response_string] for text responses
                - ["FILE", file_generator] for file transfers
                - ["GET", "FILE"] when expecting file upload
                - [] for empty/error responses
        """
        try:
            match command:
                case ["GET", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(
                        ' ', '-')
                    if self.musicFile.music_exist(music_title):
                        return ["FILE", self.musicFile.get_music(music_title)]
                    else:
                        return []
                case ["FIND", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(
                        ' ', '-')
                    if self.musicFile.music_exist(music_title):
                        answer = "FOUND FILE"
                    else:
                        answer = "NOT FOUND FILE"
                    return ["TEXT", answer]
                case ["ADD", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(
                        ' ', '-')
                    if self.musicFile.music_exist(music_title):
                        i = 1
                        music_title = f'{music_title}-{i}'
                        while self.musicFile.music_exist(music_title):
                            i += 1
                    self.musicFile.init_file(music_title)
                    return ["GET", "FILE"]
                case _:
                    return []
        except Exception as e:
            return [f"Error: {str(e)}"]

    def write_to_file(self, data):
        """Write data chunk to currently open file.

        Args:
            data: Binary data chunk to write to file
        """
        self.musicFile.write_data(data)

    def close_file_conn(self):
        """Close the current file connection and complete file operations."""
        self.musicFile.close_file()
