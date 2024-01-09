import socket
import sys
from threading import Thread
from registration import registration_thread
from list_sharing import list_sharing_thread


if __name__ == "__main__":
    if len(sys.argv) == 2:
        HOST = socket.gethostbyname(sys.argv[1])
    else:
        print("Server takes one argument: HOST")
        exit(1)

    BUFFER_SIZE = 32
    REGISTRATION_PORT = 8000
    LIST_SHARING_PORT = 8001

    registration = Thread(None, registration_thread, "registration_thread", (HOST, BUFFER_SIZE, REGISTRATION_PORT), daemon=True)
    registration.start()

    list_sharing_thread(HOST, BUFFER_SIZE, LIST_SHARING_PORT)
