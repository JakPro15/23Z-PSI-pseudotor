import socket
import sys
import time

from pseudotor_client import pseudotor_wrap


if __name__ == "__main__":
    try:
        SERVER = socket.gethostbyname(sys.argv[1])
        PORT = int(sys.argv[2])
        OVERSEER = socket.gethostbyname(sys.argv[3])

        time.sleep(2)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
            with pseudotor_wrap(
                connecting_socket, SERVER, PORT, OVERSEER
            ) as wrapped_socket:
                print(f"Sending data to address {(SERVER, PORT)}")
                wrapped_socket.sendall(b"A" * 10000 + b"END")
                data = wrapped_socket.recv(1024)
                if data == b"END":
                    wrapped_socket.sendall(b"Bye")
                    print(f"Received confirmation from {(SERVER, PORT)}. Shutting down.")
                elif data == b'':
                    print(f"Server connection aborted.")
                else:
                    print(f"Invalid confirmation of len {len(data)}: {data}")

    except Exception as e:
        print(f"Error occurred with message: {e}")
