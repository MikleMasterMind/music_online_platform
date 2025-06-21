import socket
import asyncio

class SockedWrapper:
    def __init__(self, ip: str, port: str):
        self.socket = socket.socket()
        