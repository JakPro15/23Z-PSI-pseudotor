import socket
import ssl
from contextlib import contextmanager

from exceptions import ServerUnavailableError
from middle_node_chooser import choose_middle_node

MIDDLE_NODE_PORT = 8000


@contextmanager
def pseudotor_wrap(connecting_socket: socket.socket, server_address: str, port: int, overseer_address: str) -> ssl.SSLSocket:
    connected = False
    unavailable_middle_nodes = set()
    while not connected:
        middle_node = choose_middle_node(
            overseer_address, unavailable_middle_nodes
        )
        print(f"Selected middle node: {middle_node}")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        try:
            ssl_socket = context.wrap_socket(connecting_socket)
            ssl_socket.connect((middle_node, MIDDLE_NODE_PORT))
        except Exception as e:
            unavailable_middle_nodes.add(middle_node)
            continue

        try:
            data = bytearray(socket.inet_aton(server_address))
            data.extend(port.to_bytes(2, "big", signed=False))
            ssl_socket.sendall(data)
            print("Sent server address and port number.")
            data = ssl_socket.recv(2)
        except Exception as e:
            unavailable_middle_nodes.add(middle_node)
            continue
        if data == b"OK":
            print("Connected to server.")
            connected = True
        elif data == b"NO":
            raise ServerUnavailableError("Failed to connect to the server.")
        else:
            unavailable_middle_nodes.add(middle_node)
            continue

    try:
        yield ssl_socket
    finally:
        ssl_socket.close()
