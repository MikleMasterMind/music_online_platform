from music_db.Music import Music
import asyncio
import shlex
from collections import defaultdict
from datetime import datetime
from .ConectProcessor import ConectProcessor


class MusicServer:
    def __init__(self, host='localhost', port=1337, 
                 db_host='localhost', db_user='root', db_password='', 
                 db_name='music_db', db_auth_plugin='mysql_native_password'):
        self.server = None
        self.host = host
        self.port = port
        self.music = Music(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            auth_plugin=db_auth_plugin
        )
        self.logged_users = {}  # {writer: username}
        self.connected_users = {} #{username: asyncio.Queue}
        self.registered_users = set(self.music.get_all_regisrtered_users())

    async def broadcast_timer_messages(self):
        """Рассылает сообщения всем подключенным пользователям по таймеру"""
        while True:
            await asyncio.sleep(1)  

    async def connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")

        cmdproc = ConectProcessor(self.music, self.logged_users, self.registered_users)

        try:
            while not reader.at_eof():
                command = (await reader.readline()).decode().strip()
                if not command:
                    continue
                
                response = await cmdproc.process_command(command, writer)
                username = self.logged_users.get(writer)
                # Если это команда login и она успешна, инициализируем receive_task
                if command.startswith('login ') and "Welcome" in response and username:
                    if username not in self.connected_users:
                        self.connected_users[username] = asyncio.Queue()
                    
                if username and username in self.connected_users:
                    await self.connected_users[username].put(response)
                else:
                    await self.send_to_user(writer, response)     

        except ConnectionError:
            print(f"Client {addr} disconnected")
        finally:
            if username in self.connected_users:
                del self.connected_users[username]
            if writer in self.logged_users:
                del self.logged_users[writer]
                
            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()
    
    async def _message_dispatcher(self):
        """Processes messages for a specific user"""
        while True:
            for username, queue in list(self.connected_users.items()):
                try:
                    while not queue.empty():
                        message = await queue.get()
                        writer = next((w for w, u in self.logged_users.items() if u == username), None)
                        if writer and not writer.is_closing():
                            await self.send_to_user(writer, message)
                except (ConnectionError, KeyError):
                    continue
            await asyncio.sleep(0.1)
    
    async def sayall(self, message, me=None):
        """
        Send a message to all connected users except the sender.

        Args
        ----
        message : str
            The message to be sent to all users.
        me : str
            The name of the user who is sending the message.
        """
        for username in list(self.connected_users.keys()):
            if username != me and username in self.connected_users:
                await self.connected_users[username].put(message)
    
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

    async def start(self):
        self.server = await asyncio.start_server(self.connection, self.host, self.port)
        asyncio.create_task(self._message_dispatcher())
        print(f"Music server started on {self.host}:{self.port}")
        async with self.server:
            await self.server.serve_forever()