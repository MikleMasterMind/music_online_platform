"""Server for music platform."""

import asyncio
import shlex
from .ConectProcessor import ConectProcessor


class MusicServer:
    """Server for handling music requests and managing client connections."""

    def __init__(self, musicSql_db, musicFile_db, host='localhost', port=1337):
        """Initialize the music server with specified parameters.

        Args:
            musicSql_db: SQL database for storing music metadata
            musicFile_db: File storage for music files
            host (str): Host address to bind to (default 'localhost')
            port (int): Port number to listen on (default 1337)
        """
        self.server = None
        self.host = host
        self.port = port
        self.musicSQL_db = musicSql_db
        self.musicFile_db = musicFile_db
        self.logged_users: dict = {}  # {writer: user_tmp_id}
        self.connected_users: dict = {}  # {user_tmp_id: asyncio.Queue}
        self.users_count = 0

    async def connection(self, reader, writer):
        """Handle a new client connection.

        Processes incoming commands from the client \
            and manages the connection lifecycle.

        Args:
            reader: StreamReader for incoming data
            writer: StreamWriter for outgoing data
        """
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")

        cmdproc = ConectProcessor(
            self.musicSQL_db,
            self.musicFile_db,
            self.logged_users)

        user_tmp_id = self.users_count
        self.users_count += 1
        self.connected_users[user_tmp_id] = asyncio.Queue()
        if self.users_count > 10**6:
            self.users_count = 0

        try:
            while not reader.at_eof():
                command = \
                    shlex.split((await reader.readline()).decode().strip())
                print(f'{command=}')
                if not command:
                    continue

                response = await cmdproc.process_command(command, writer)
                print(f'{response=}')
                if len(response) == 0:
                    await self.send_to_user(writer, "ERROR")
                if response[0] == "TEXT":
                    await self.send_to_user(writer, response[1])
                elif response[0] == "FILE":
                    await self.send_to_user(writer, "FILE TRANSMIT")
                    await self.send_file(writer, response[1])
                elif response[0] == "GET":
                    size = int((await reader.readline()).decode().strip())
                    print(f'{size=}')
                    chunk_size = 4096
                    while size >= 0:
                        chunk = await reader.read(chunk_size)
                        cmdproc.write_to_file(chunk)
                        chunk = min(chunk_size, size)
                        size -= chunk_size
                    cmdproc.close_file_conn()

        except ConnectionError:
            print(f"Client {addr} disconnected")
        finally:
            del self.connected_users[user_tmp_id]
            if writer in self.logged_users:
                del self.logged_users[writer]

            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()

    async def _message_dispatcher(self):
        """Process and dispatch messages from queues to appropriate users.

        Continuously checks message queues for all connected users
        and forwards messages to their respective writers.
        """
        while True:
            for user_tmp_id, queue in list(self.connected_users.items()):
                try:
                    while not queue.empty():
                        message = await queue.get()
                        writer = next(
                            (w for w, u in self.logged_users.items() if u == user_tmp_id), None)
                        if writer and not writer.is_closing():
                            await self.send_to_user(writer, message)
                except (ConnectionError, KeyError):
                    continue
            await asyncio.sleep(0.1)

    async def send_to_user(self, writer, message):
        """Send a text message to a specific connected user.

        Args:
            writer: The StreamWriter object for the target user
            message: The message string to send

        Returns:
            None
        """
        writer.write(f"{message}\n".encode())
        await writer.drain()

    async def send_file(self, writer, file_generator):
        """Stream a file to the connected user.

        Args:
            writer: The StreamWriter object for the target user
            file_generator: Generator yielding file chunks

        Returns:
            None
        """
        for chunk in file_generator:
            writer.write(chunk)
        await writer.drain()

    async def start(self):
        """Start the music server and begin accepting connections.

        Initializes the server and message dispatcher,
        then enters the main serving loop.
        """
        self.server = \
            await asyncio.start_server(self.connection, self.host, self.port)
        asyncio.create_task(self._message_dispatcher())
        print(f"Music server started on {self.host}:{self.port}")
        async with self.server:
            await self.server.serve_forever()
