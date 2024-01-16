import socket
import sys
from threading import Thread

from request_handling import handle_request


if __name__ == "__main__":
    if len(sys.argv) == 2:
        HOST = socket.gethostbyname(sys.argv[1])
    else:
        print("Overseer server takes one argument: HOST - own hostname")
        exit(1)

    BUFFER_SIZE = 32
    PORT = 8001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((HOST, PORT))
        listening_socket.listen(5)
        print(f"Overseer open on address {(HOST, PORT)}")
        while True:
            conn, addr = listening_socket.accept()
            Thread(
                None,
                handle_request,
                None,
                (conn, addr, BUFFER_SIZE),
                daemon=True,
            ).start()
