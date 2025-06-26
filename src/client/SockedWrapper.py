"""Socket wrapper with busy channel tracking."""

import socket


class SockedWrapper:
    """Wraps a socket with enhanced functionality.

    Provides:
    - Line-based reading
    - Busy channel tracking
    - Convenient encoding/decoding
    - Raw byte operations
    """

    def __init__(self, host: str, port: int):
        """Initialize and connect to a TCP socket.

        Args:
            host: Hostname or IP address to connect to
            port: TCP port number to connect to
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.channel_busy = False

    def recv(self, size: int):
        """Receive data from the socket with busy state tracking.

        Args:
            size: Maximum number of bytes to receive

        Returns:
            bytes: Received data
        """
        self.channel_busy = True
        result = self.socket.recv(size)
        self.channel_busy = False
        return result

    def readline(self):
        """Read a line of text from the socket.

        Returns:
            str: Decoded string without trailing newline

        Note:
            - Reads until newline character
            - Sets channel_busy flag during operation
            - Strips whitespace from result
        """
        self.channel_busy = True
        buffer = bytearray()
        while char := self.socket.recv(1):
            if char == b'\n':
                break
            buffer.extend(char)
        self.channel_busy = False
        return buffer.decode().strip()

    def sendall(self, data: str):
        """Send complete string data (encoded to bytes).

        Args:
            data: String to send
        """
        self.socket.sendall(data.encode())

    def send(self, data: str):
        """Send string data (encoded to bytes).

        Args:
            data: String to send
        """
        self.socket.send(data.encode())

    def busy(self) -> bool:
        """Check if channel is currently busy."""
        return self.channel_busy

    def sendraw(self, data: bytes):
        """Send raw byte data without encoding.

        Args:
            data: Bytes to send directly to socket
        """
        self.socket.send(data)
