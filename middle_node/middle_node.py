import socket
import ssl
from typing import Tuple

from middle_node.connection_server import ConnectionServer
from middle_node.registrant_thread import RegistrantThread


class MiddleNode:
    def __init__(
        self,
        address: Tuple[str, int],
        overseer: Tuple[str, int],
        max_delay: float,
        new_segmentation_range: Tuple[int, int] | None,
    ):
        self.address = address
        self.max_delay = max_delay
        self.segmentation_range = new_segmentation_range
        self.registrant_thread = RegistrantThread(overseer, 10)
        self.registrant_thread.start()
        self.server = ConnectionServer()
        # TODO: set up real context
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def run(self):
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as listening_socket:
            with self.context.wrap_socket(
                listening_socket, server_side=True
            ) as ssl_socket:
                ssl_socket.bind(self.address)
                ssl_socket.listen(5)
                while True:
                    conn, addr = ssl_socket.accept()
                    conn.close()
                    self.server.add_connection(addr, self.context)
                    self.server.remove_old_connections()


if __name__ == "__main__":
    middle_node = MiddleNode(("127.0.0.1", 8002), ("127.0.0.1", 8001), 0, None)
    middle_node.run()
