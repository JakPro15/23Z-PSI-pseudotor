from threading import Thread
import ssl
import socket

from forwarder import Forwarder
from registrant_thread import RegistrantThread


def handle_connection(client_socket: ssl.SSLSocket):
    with client_socket:
        data = client_socket.recv(6)
        server_address = socket.inet_ntoa(data[:4])
        server_port = int.from_bytes(data[4:6], byteorder='big', signed=False)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((server_address, server_port))
            Forwarder(client_socket, server_socket).run()


def add_connection(client_socket: ssl.SSLSocket):
    Thread(
        target=handle_connection,
        args=(client_socket,),
        daemon=True,
    ).start()


# HOST = 'localhost'
# PORT = 8000
# if __name__ == '__main__':
#     RegistrantThread('localhost', 3 * 60).start()
#     context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#     context.load_cert_chain('certfile.pem', 'keyfile.key', password='bruh')
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
#         with context.wrap_socket(listening_socket, server_side=True) as ssl_socket:
#             ssl_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#             ssl_socket.bind((HOST, PORT))
#             ssl_socket.listen(5)
#             print(f"Waiting for data on address {(HOST, PORT)}")
#             while True:
#                 conn, addr = ssl_socket.accept()
#                 add_connection(conn)
