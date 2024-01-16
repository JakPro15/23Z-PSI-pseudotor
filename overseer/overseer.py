import socket
import sys
from threading import Thread
from request_handling import handle_request

if __name__ == "__main__":
    if len(sys.argv) == 2:
        HOST = socket.gethostbyname(sys.argv[1])
    else:
        print("Server takes one argument: HOST")
        exit(1)

    BUFFER_SIZE = 32
    PORT = 8001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind((HOST, PORT))
        listening_socket.listen(5)
        print("Waiting for list sharing requests")
        while True:
            conn, addr = listening_socket.accept()
            handler = Thread(None, handle_request, None, (conn, addr, BUFFER_SIZE), daemon=True)
            handler.start()
