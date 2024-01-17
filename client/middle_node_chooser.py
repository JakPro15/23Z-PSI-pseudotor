import socket
from random import choice
from exceptions import OverseerUnavailableError, MiddleNodeUnavailableError


LIST_SHARING_PORT = 8001
BUFFER_SIZE = 1024


def _get_middle_node_list(overseer_address: str) -> list[str]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as overseer_socket:
            overseer_socket.connect((overseer_address, LIST_SHARING_PORT))
            overseer_socket.sendall(b"PSEUDOTOR_GET_NODES")
            received = bytearray()
            data = overseer_socket.recv(BUFFER_SIZE)
            while data != b'':
                received.extend(data)
                data = overseer_socket.recv(BUFFER_SIZE)
            return received.decode('ascii').split(" ")[:-1]
    except Exception as e:
        raise OverseerUnavailableError("Failed to obtain middle nodes list from overseer.") from e


def choose_middle_node(overseer_address: str) -> str:
    middle_nodes = _get_middle_node_list(overseer_address)
    if len(middle_nodes) == 0:
        raise MiddleNodeUnavailableError("No PseudoTor middle nodes are registered.")
    return choice(middle_nodes)
