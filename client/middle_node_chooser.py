import socket
from random import choice

LIST_SHARING_PORT = 8001
CHOOSER_BUFFER_SIZE = 32

def _get_middle_node_list(ip_address: str, buffer_size: int) -> list[str]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        connecting_socket.connect((ip_address, LIST_SHARING_PORT))
        connecting_socket.sendall(b"PSEUDOTOR_GET_NODES")
        return connecting_socket.recv(CHOOSER_BUFFER_SIZE).decode('ascii').split(" ")

def choose_middle_node(ip_address: str) -> str:
    return choice(_get_middle_node_list(ip_address, CHOOSER_BUFFER_SIZE))