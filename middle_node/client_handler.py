import socket
import ssl
from typing import Tuple


class ClientHandler:
    def __init__(self, address: Tuple[str, int], context: ssl.SSLContext):
        self.address = address
        self.context = context

    def get_server_and_data(self) -> Tuple[str, bytes]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with self.context.wrap_socket(sock, server_side=True) as ssl_sock:
                ssl_sock.connect(self.address)
                received_data = ssl_sock.recv(1024)
                server_address = received_data[:4].decode("ascii")
                data = received_data[4:]
                return (server_address, data)

    def send_to_client(self, data: bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with self.context.wrap_socket(sock, server_side=True) as ssl_sock:
                ssl_sock.connect(self.address)
                ssl_sock.sendall(data)
