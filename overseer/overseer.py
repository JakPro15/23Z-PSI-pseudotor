import socket
import sys
from threading import Thread
import argparse

from request_handling import handle_request


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("own_address")
    args = parser.parse_args()

    HOST = socket.gethostbyname(args.own_address)
    BUFFER_SIZE = 32
    PORT = 8001

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listening_socket.bind((HOST, PORT))
            listening_socket.listen(5)
            print(f"Overseer open on address {(HOST, PORT)}")
            while True:
                try:
                    conn, addr = listening_socket.accept()
                except Exception as e:
                    print(f"Error accepting a connection. Error message: {e}")
                    break
                try:
                    Thread(
                        None,
                        handle_request,
                        None,
                        (conn, addr, BUFFER_SIZE),
                        daemon=True,
                    ).start()
                except Exception as e:
                    print(f"Error starting thread to handle connection. Error message: {e}")
                    break
    except Exception as e:
        print(f"Error starting overseer server. Error message: {e}")
