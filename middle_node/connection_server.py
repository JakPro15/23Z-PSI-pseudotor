import collections
from ssl import SSLContext
from threading import Thread
from typing import Dict, Tuple

from client_handler import ClientHandler

from middle_node.server_handler import ServerHandler


def handle_connection(address: Tuple[str, int], context: SSLContext):
    client_handler = ClientHandler(address, context)
    addr, data = client_handler.get_server_and_data()
    server_handler = ServerHandler((addr, 8000))
    server_handler.send(data)
    response = server_handler.receive()
    client_handler.send_to_client(response)


class ConnectionServer:
    def __init__(self):
        self.threads: Dict[Tuple[str, int], Thread] = {}

    def add_connection(self, address: Tuple[str, int], context: SSLContext):
        assert address not in self.threads
        handler = Thread(
            target=handle_connection,
            args=(address, context),
            daemon=True,
        )
        handler.start()
        self.threads[address] = handler

    def remove_old_connections(self):
        self.threads = {k: v for k, v in self.threads.items() if v.is_alive()}
