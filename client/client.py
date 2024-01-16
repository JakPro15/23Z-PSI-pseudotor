import sys
import socket
from pseudotor_client import pseudotor_wrap

if __name__ == "__main__":
    if len(sys.argv) == 4:
        SERVER = socket.gethostbyname(sys.argv[1])
        SERVER_PORT = int(sys.argv[2])
        OVERSEER = socket.gethostbyname(sys.argv[3])
    else:
        print("Client takes three arguments: SERVER, SERVER_PORT, OVERSEER")
        exit(1)

    BUFFER_SIZE = 1024

    data = b"Hello!"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        with pseudotor_wrap(connecting_socket, SERVER, SERVER_PORT, OVERSEER) as pt_socket:
            pt_socket.sendall(data)
            pt_socket.sendall(b'END')

            response_buffer = bytearray()
            while True:
                response = pt_socket.recv(BUFFER_SIZE)
                if not response:
                    break
                response_buffer.extend(response)

            print(f"Data: {data}")
            print(f"Response: {bytes(response_buffer)}")

