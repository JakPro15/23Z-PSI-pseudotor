import ssl
import socket
from middle_node_chooser import choose_middle_node

MIDDLE_NODE_PORT = 8002

def get_data_from_server(destination_address: str, overseer_address: str, data: str, buffer_size: int) -> str:
    print("Selecting middle node")
    middle_node = choose_middle_node(overseer_address, buffer_size)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
        with context.wrap_socket(connecting_socket, server_hostname='127.0.0.1') as ssl_socket:
            ssl_socket.connect((middle_node, MIDDLE_NODE_PORT))
            print("Sending server address")
            ssl_socket.sendall(destination_address.encode())
            response = ssl_socket.recv(buffer_size)

            if response != b'Received address. Provide data':
                raise ValueError('Error in sending server address')
            
            print("Sending data")
            ssl_socket.sendall(data)
            return ssl_socket.recv(buffer_size)