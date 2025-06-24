import socket


class SockedWrapper:
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.channel_busy = False

    def recv(self, size: int):
        self.channel_busy = True
        result = self.socket.recv(size)
        self.channel_busy = False
        return result

    def readline(self):
        self.channel_busy = True
        buffer = bytearray()
        while char := self.socket.recv(1):
            if char == b'\n':
                break
            buffer.extend(char)
        self.channel_busy = False
        return buffer.decode().strip()

    def sendall(self, data: str):
        self.socket.sendall(data.encode())
    
    def send(self, data: str):
        self.socket.send(data.encode())

    def busy(self) -> bool:
        return self.channel_busy
    
    def sendraw(self, data: bytes):
        self.socket.send(data)