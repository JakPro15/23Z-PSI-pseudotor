import socket
import sys
from threading import Thread


def handle_client(conn, addr):
    buffer = bytearray()
    try:
        with conn:
            print(f"Connected to {addr}")
            data = conn.recv(10003)
            buffer.extend(data)
            print(f"Received {len(data)} bytes of data from {addr}")
            while b"END" not in buffer:
                data = conn.recv(10003)
                buffer.extend(data)
                if data == b'':
                    print("Client connection aborted.")
                    return
                print(f"Received {len(data)} bytes of data from {addr}")
            conn.sendall(b"END")
            print(f"Sent confirmation to {addr}")
            data = conn.recv(3)
            print(f"Received {data}")
    except Exception as e:
        print(f"An error occurred in communication with {addr}: {e}")


if __name__ == "__main__":
    try:
        HOST = socket.gethostbyname(sys.argv[1])
        PORT = int(sys.argv[2])

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
            listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listening_socket.bind((HOST, PORT))
            listening_socket.listen(5)
            print(f"Waiting for data on address {(HOST, PORT)}")
            while True:
                try:
                    conn, addr = listening_socket.accept()
                    Thread(None, handle_client, None, (conn, addr), daemon=True).start()
                except Exception as e:
                    print(f"Error accepting connection: {e}")
    except Exception as e:
        print(f"Error in server: {e}")
