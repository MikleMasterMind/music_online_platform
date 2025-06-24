import asyncio
import shlex
from collections import defaultdict
from datetime import datetime
from .ConectProcessor import ConectProcessor


class MusicServer:
    def __init__(self, musicSql_db, musicFile_db, host='localhost', port=1337):
        self.server = None
        self.host = host
        self.port = port
        self.musicSQL_db = musicSql_db
        self.musicFile_db = musicFile_db
        self.logged_users : dict = {}  # {writer: user_tmp_id}
        self.connected_users : dict = {} #{user_tmp_id: asyncio.Queue}
        self.users_count = 0

    async def broadcast_timer_messages(self):
        """Рассылает сообщения всем подключенным пользователям по таймеру."""
        while True:
            await asyncio.sleep(1)

    async def connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")

        cmdproc = ConectProcessor(self.musicSQL_db, self.musicFile_db, self.logged_users)

        username = None
        user_tmp_id = self.users_count
        self.users_count += 1
        self.connected_users[user_tmp_id] = asyncio.Queue()
        if self.users_count > 10**6:
            self.users_count = 0

        try:
            while not reader.at_eof():
                command = shlex.split((await reader.readline()).decode().strip())
                if not command:
                    continue
                
                response = await cmdproc.process_command(command, writer)
                if response[0] == "TEXT":
                    await self.send_to_user(writer, response[1])
                elif response[0] == "FILE":
                    await self.send_to_user(writer, "FILE TRANSMIT")
                    await self.send_file(writer, response[1])
                else:
                    await self.send_to_user(writer, "ERROR")

                # username = self.logged_users.get(writer)
                    
                # if username and username in self.connected_users:
                #     await self.connected_users[username].put(response)
                # else:
                #     await self.send_to_user(writer, response)     

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
        """Processes messages for a specific user."""
        while True:
            for user_tmp_id, queue in list(self.connected_users.items()):
                try:
                    while not queue.empty():
                        message = await queue.get()
                        writer = next((w for w, u in self.logged_users.items() if u == user_tmp_id), None)
                        if writer and not writer.is_closing():
                            await self.send_to_user(writer, message)
                except (ConnectionError, KeyError):
                    continue
            await asyncio.sleep(0.1)
    
    async def send_to_user(self, writer, message):
        """
        Send a message to a connected user.

        Args
        ----
        writer : StreamWriter
            The writer to send the message.
        message : str
            The message to send.
        """
        writer.write(f"{message}\n".encode())
        await writer.drain()
    
    async def send_file(self, writer, file_generator):
        for chunk in file_generator:
            writer.write(chunk)
        await writer.drain()

    async def start(self):
        self.server = await asyncio.start_server(self.connection, self.host, self.port)
        asyncio.create_task(self._message_dispatcher())
        print(f"Music server started on {self.host}:{self.port}")
        async with self.server:
            await self.server.serve_forever()