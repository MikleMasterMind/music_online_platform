import cmd
import shlex
import socket
import time
import threading
class Music_User(cmd.Cmd):
    intro = '<<< Welcome to Music App 1.0 >>>'
    prompt = '(music) '

    def __init__(self, socket: socket.socket):
        super().__init__()
        self.socket = socket
        self.current_user = None

        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_messages, daemon=True)
        self.receive_thread.start()

    def _receive_messages(self):
        """Background thread for receiving messages from the server."""
        while self.running :
            try:
                message = self.get_msg()
                if message:
                    print(f"{message}\n{self.prompt}", end=' ', flush=True)
            except (ConnectionError, OSError):
                if self.running :
                    print("\nConnection lost with server")
                    self.running  = False
                break

    def get_msg(self) -> str:
        """
        Receive and return a message from the server.

        Returns
        -------
            str: Received message from server.
        """
        response = self.socket.recv(1024).decode().strip()
        return response

    def send_msg(self, message: str) -> None:
        """
        Send a message to the server.

        Args:
            message (str): Message to send.
        """
        time.sleep(1)
        self.socket.sendall(f'{message}\n'.encode())

    def do_registration(self, arg):
        """Register new user: registration <username> <name> <password>"""
            
        args = shlex.split(arg)
        if len(args) != 3:
            print("Usage: registration <username> <name> <password>")
            print("Example: registration john_doe John secret123")
            return
            
        username, name, password = args
        self.send_msg(f"registration {username} {name} {password}")

    def do_login(self, arg):
        """Login to the system: login <username> <password>"""
            
        args = shlex.split(arg)
        if len(args) != 2:
            print("Usage: login <username> <password>")
            return
            
        self.send_msg(f"login {args[0]} {args[1]}")
    
    def do_exit(self, arg):
        """Exit the application"""
        self.do_logout("")
        self.running = False
        self.socket.close()
        print("Goodbye!")
        return True
    
    def do_logout(self, arg):
        """Logout from the system""" 
        self.send_msg("logout")