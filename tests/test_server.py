import unittest
import socket
import time
import asyncio
from src.server.MusicServer import MusicServer
from src.music_db.MusicFileDB import MusicFileDB
from src.server import __main__
import multiprocessing


class TestMusicServerReal(unittest.TestCase):
    """Real socket-based tests for MusicServer"""

    @classmethod
    def setUpClass(cls):
        """Start the server in a separate thread"""
        server = MusicServer(None, MusicFileDB(path_to_mp3 = "./src/music_db/data"), host='0.0.0.0', port=1337)
        cls.proc = multiprocessing.Process(target=__main__.start)
        cls.proc.start()
        time.sleep(1)
        cls.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.socket.connect(('localhost', 1337))

    @classmethod
    def tearDownClass(cls):
        """Clean up server"""
        cls.socket.close()
        time.sleep(0.5)
        cls.socket.close()
        cls.proc.terminate()


    def send_command(self, command):
        """Helper to send command and get response"""
        self.socket.sendall((command + '\n').encode())
        return self.socket.recv(4096).decode().strip()


    def test_find_file_command(self):
        """Test FIND FILE command"""
        response = self.send_command("FIND FILE unknown.mp3")
        self.assertEqual(response, "NOT FOUND FILE")


    def test_multiple_connections(self):
        """Test multiple simultaneous connections"""
        sockets = []
        try:
            for i in range(3):  # Create 3 connections
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('localhost', 1337))
                sockets.append(sock)
                time.sleep(0.1)
            
            for sock in sockets:
                sock.sendall(b"FIND FILE test.mp3\n")
                response = sock.recv(4096).decode().strip()
                self.assertIn(response, ["FOUND FILE", "NOT FOUND FILE"])
        finally:
            for sock in sockets:
                sock.close()

if __name__ == '__main__':
    unittest.main()