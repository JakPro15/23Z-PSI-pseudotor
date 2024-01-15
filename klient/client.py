import sys
import socket
from threading import Thread
from pseudotor_client import tunnel_data

if __name__ == "__main__":
    if len(sys.argv) == 3:
        OVERSEER = socket.gethostbyname(sys.argv[1])
        TIMEOUT = float(sys.argv[2])
    else:
        print("Client takes two arguments: OVERSEER and timeout [s]")
        exit(1)

    BUFFER_SIZE = 4096
    CLIENT_PORT = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind(('127.0.0.1', CLIENT_PORT))
        listening_socket.listen(5)
        print(f"PseudoTor client listening on port: {CLIENT_PORT}")
        while True:
            conn, addr = listening_socket.accept()
            handler = Thread(None, tunnel_data, None, (conn, OVERSEER, BUFFER_SIZE, TIMEOUT), daemon=True)
            handler.start()
