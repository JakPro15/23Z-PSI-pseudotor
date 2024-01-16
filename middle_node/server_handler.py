import socket
from typing import Tuple


class ServerHandler:
    def __init__(self, server_address: Tuple[str, int]):
        self.server_address = server_address

    def send(self, data: bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            sock.sendall(data)

    def receive(self) -> bytes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(self.server_address)
            return sock.recv(1024)
