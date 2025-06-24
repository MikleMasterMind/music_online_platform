import socket


class SockedWrapper:
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def recv(self, size: int):
        return self.socket.recv(size)

    def readline(self):
        buffer = bytearray()
        while char := self.socket.recv(1):
            if char == b'\n':
                break
            buffer.extend(char)
        return buffer.decode().strip()

    def sendall(self, data: str):
        self.socket.sendall(data.encode())
    
    def send(self, data: str):
        self.socket.send(data.encode())
