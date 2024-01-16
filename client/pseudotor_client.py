import ssl
import socket
from middle_node_chooser import choose_middle_node
from contextlib import contextmanager

MIDDLE_NODE_PORT = 8000

@contextmanager
def pseudotor_wrap(connecting_socket: socket.socket, server_address: str, port: int, overseer_address: str):
    middle_node = choose_middle_node(overseer_address)
    print(f"Selected middle node: {middle_node}")

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    ssl_socket = context.wrap_socket(connecting_socket)
    ssl_socket.connect((middle_node, MIDDLE_NODE_PORT))
    data = bytearray(socket.inet_aton(server_address))
    data.extend(port.to_bytes(2, 'big', signed=False))
    ssl_socket.sendall(data)
    print("Sent server address and port number")

    try:
        yield ssl_socket
    finally:
        ssl_socket.close()
