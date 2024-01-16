import socket
import ssl

from middle_node_chooser import choose_middle_node

MIDDLE_NODE_PORT = 8002


def tunnel_data(
    conn: socket.socket, overseer_address: str, buffer_size: int, timeout: float
):
    with conn:
        conn.settimeout(timeout)
        print("Pseudotor connected")

        middle_node = choose_middle_node(overseer_address, buffer_size)
        print("Selected middle node")

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as connecting_socket:
            with context.wrap_socket(connecting_socket) as ssl_socket:
                ssl_socket.connect((middle_node, MIDDLE_NODE_PORT))
                ssl_socket.settimeout(timeout)

                client_data_buffer = bytearray()
                server_data_buffer = bytearray()

                while True:
                    try:
                        client_data = conn.recv(buffer_size)
                    except TimeoutError:
                        client_data = b""

                    try:
                        server_data = ssl_socket.recv(buffer_size)
                    except TimeoutError:
                        server_data = b""

                    print(f"{client_data=}")
                    print(f"{server_data=}")

                    if (
                        len(client_data_buffer) == 0
                        and len(server_data_buffer) == 0
                    ):
                        break

                    if not client_data and len(client_data_buffer) > 0:
                        ssl_socket.sendall(client_data_buffer)
                        client_data_buffer = bytearray()
                    elif (
                        len(client_data_buffer) + len(client_data) > buffer_size
                    ):
                        ssl_socket.sendall(client_data_buffer)
                        client_data_buffer = bytearray()
                    client_data_buffer.extend(client_data)

                    if not server_data and len(server_data_buffer) > 0:
                        conn.sendall(server_data_buffer)
                        server_data_buffer = bytearray()
                    elif (
                        len(server_data_buffer) + len(server_data) > buffer_size
                    ):
                        conn.sendall(server_data_buffer)
                        server_data_buffer = bytearray()
                    server_data_buffer.extend(server_data)
    conn.close()
