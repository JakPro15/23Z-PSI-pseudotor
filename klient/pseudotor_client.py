import ssl
import socket
from middle_node_chooser import choose_middle_node

MIDDLE_NODE_PORT = 8002

def get_data_from_server(overseer_address: str, data: bytes, buffer_size: int) -> str:
    print("Selecting middle node")
    middle_node = choose_middle_node(overseer_address, buffer_size)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        with context.wrap_socket(connecting_socket) as ssl_socket:
            ssl_socket.connect((middle_node, MIDDLE_NODE_PORT))
            print("Sending server address and data")
            ssl_socket.sendall(data)
            return ssl_socket.recv(buffer_size)

  
def tunnel_data(conn: socket.socket, overseer_adress: str, buffer_size: int):
    with conn:
        print("Pseudotor connected")
        data = conn.recv(buffer_size)
        response = get_data_from_server(overseer_adress, data, buffer_size)
        print("Pseudotor response sent")
        conn.sendall(response)
    conn.close()