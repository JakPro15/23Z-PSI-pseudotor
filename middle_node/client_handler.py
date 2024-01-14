import socket
import ssl
from typing import Tuple


class ClientHandler:
    def __init__(self, address: Tuple[str, int]):
        self.address = address
        # TODO: set the context to the final SSL certificate values
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def receive_and_unpack(self) -> Tuple[str, bytes]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            with self.context.wrap_socket(sock, server_side=True) as ssl_sock:
                ssl_sock.bind(self.address)
                ssl_sock.listen(1)
                conn, _ = ssl_sock.accept()
                with conn:
                    server_address = conn.recv(1024).decode("ascii")
                    conn.sendall(b"Received address. Provide data")
                    data = conn.recv(1024)
                    return (server_address, data)
