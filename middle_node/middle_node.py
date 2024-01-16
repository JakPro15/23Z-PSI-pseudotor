import argparse
import socket
import ssl
import time

from connection_handling import add_connection
from registrant_thread import RegistrantThread


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
        try:
            RegistrantThread("localhost", REGISTRATION_PERIOD).start()
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain("certfile.pem", "keyfile.key", password="bruh")
            with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            ) as listening_socket:
                with context.wrap_socket(
                    listening_socket, server_side=True
                ) as ssl_socket:
                    ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    ssl_socket.bind(self.address)
                    ssl_socket.listen(5)
                    print(f"Waiting for data on address {self.address}")
                    while True:
                        conn, addr = ssl_socket.accept()
                        print(f"Connected to {addr}")
                        add_connection(conn, self.modification_params)

        except ssl.SSLError as e:
            print(f"SSL error in MiddleNode.run: {e}")
        except socket.error as e:
            print(f"Socket error in MiddleNode.run: {e}")
        except Exception as e:
            print(f"An unexpected error occurred in MiddleNode.run: {e}")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("own_address", nargs=1)
        parser.add_argument("overseer_address", nargs=1)
        parser.add_argument("--max_delay", "-t", type=float, required=True)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--segsize", "-ss", nargs=2, metavar=("MIN_SEG", "MAX_SEG"), type=int
        )
        group.add_argument("--no-segmentation-change", "-ns", action="store_true")
        args = parser.parse_args()
        if args.segsize:
            if args.segsize[0] <= 0:
                print("Segmentation param has to be positive")
                exit(1)
            if args.segsize[0] > args.segsize[1]:
                print("MIN_SEG has to be less than MAX_SEG")
                exit(2)

        HOST = socket.gethostbyname(args.own_address[0])
        OVERSEER = socket.gethostbyname(args.overseer_address[0])

        middle_node = MiddleNode(HOST, OVERSEER, args.max_delay, args.segsize)
        time.sleep(1)
        middle_node.run()

    except KeyboardInterrupt:
        print("MiddleNode terminated by user.")
    except Exception as e:
        print(f"An unexpected error occurred in __main__: {e}")
