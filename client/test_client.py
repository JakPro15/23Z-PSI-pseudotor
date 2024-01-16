import sys
import socket


if __name__ == "__main__":
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        connecting_socket.connect((HOST, PORT))
        print(f"Sending data to address {(HOST, PORT)}")
        connecting_socket.sendall(b'A' * 10000 + b'END')
        data = connecting_socket.recv(1024)
        if data == b'END':
            print(f"Received confirmation from {(HOST, PORT)}. Shutting down.")
