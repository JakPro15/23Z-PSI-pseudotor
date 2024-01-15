import sys
import socket
from threading import Thread
from pseudotor_client import tunnel_data

if __name__ == "__main__":
    if len(sys.argv) == 2:
        OVERSEER = socket.gethostbyname(sys.argv[1])
    else:
        print("Client takes one argument: OVERSEER")
        exit(1)

    BUFFER_SIZE = 4096
    CLIENT_PORT = 8000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind(('127.0.0.1', CLIENT_PORT))
        listening_socket.listen(5)
        print(f"Listening on port: {CLIENT_PORT}")
        print(f"Message format: server (4 bytes), data (max. 4092 bytes)")
        while True:
            conn, addr = listening_socket.accept()
            handler = Thread(None, tunnel_data, None, (conn, OVERSEER, BUFFER_SIZE), daemon=True)
            handler.start()
