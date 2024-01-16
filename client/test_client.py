import sys
import socket
from pseudotor_client import pseudotor_wrap


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        with pseudotor_wrap(connecting_socket, HOST, PORT, '127.0.0.1') as wrapped_socket:
            print(f"Sending data to address {(HOST, PORT)}")
            wrapped_socket.sendall(b'A' * 10000 + b'END')
            data = wrapped_socket.recv(1024)
            if data == b'END':
                wrapped_socket.sendall(b'Bye')
                print(f"Received confirmation from {(HOST, PORT)}. Shutting down.")
            else:
                print(f"Invalid confirmation of len {len(data)}: {data}")
