from threading import Thread
import ssl
import socket

from forwarder import Forwarder


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
