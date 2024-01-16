import sys
import socket
from pseudotor_client import get_data_from_server

if __name__ == "__main__":
    if len(sys.argv) == 3:
        SERVER = socket.gethostbyname(sys.argv[1])
        OVERSEER = socket.gethostbyname(sys.argv[2])
    else:
        print("Client takes three arguments: SERVER, OVERSEER")
        exit(1)

    BUFFER_SIZE = 1024

    data = b"Hello!"

    response = get_data_from_server(OVERSEER, SERVER, data, BUFFER_SIZE)

    print(f"Data: {data}")
    print(f"Response: {response}")

