import ssl
import socket
import argparse

from registrant_thread import RegistrantThread
from connection_handling import add_connection


REGISTRATION_PERIOD = 3 * 60  # seconds

class MiddleNode:
    def __init__(
        self,
        own_address: str,
        overseer_address: str,
        max_delay: float,
        new_segmentation_range: tuple[int, int] | None,
    ):
        self.address = (own_address, 8000)
        self.modification_params = (max_delay, new_segmentation_range)
        RegistrantThread(overseer_address, 10).start()
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE


    def run(self):
        RegistrantThread('localhost', REGISTRATION_PERIOD).start()
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
                    add_connection(conn, self.modification_params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_delay', '-t', type=float, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--segsize', '-ss', nargs=2, metavar=('MIN_SEG', 'MAX_SEG'), type=int)
    group.add_argument('--no-segmentation-change', '-ns', action='store_true')
    args = parser.parse_args()
    if args.segsize:
        assert args.segsize[0] > 0
        assert args.segsize[0] <= args.segsize[1]

    middle_node = MiddleNode("127.0.0.1", "127.0.0.1", args.max_delay, args.segsize)
    middle_node.run()
