import ssl
import socket

from registrant_thread import RegistrantThread
from connection_server import add_connection


class MiddleNode:
    def __init__(
        self,
        address: tuple[str, int],
        overseer: tuple[str, int],
        max_delay: float,
        new_segmentation_range: tuple[int, int] | None,
    ):
        self.address = address
        self.max_delay = max_delay
        self.segmentation_range = new_segmentation_range
        self.registrant_thread = RegistrantThread(overseer, 10)
        self.registrant_thread.start()
        # TODO: set up real context
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE


    def run(self):
        RegistrantThread('localhost', 3 * 60).start()
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('certfile.pem', 'keyfile.key', password='bruh')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            with context.wrap_socket(listening_socket, server_side=True) as ssl_socket:
                ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                ssl_socket.bind(self.address)
                ssl_socket.listen(5)
                print(f"Waiting for data on address {self.address}")
                while True:
                    conn, addr = ssl_socket.accept()
                    print(f"Connected to {addr}")
                    add_connection(conn)


if __name__ == "__main__":
    middle_node = MiddleNode(("127.0.0.1", 8000), ("127.0.0.1", 8001), 0, None)
    middle_node.run()
