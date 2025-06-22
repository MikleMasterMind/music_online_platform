import socket
import shlex
from .Music_User import Music_User


def main(host='localhost', port= 1337):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        Music_User(s).cmdloop()

if __name__ == "__main__":
    main() 