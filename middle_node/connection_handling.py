from threading import Thread
import ssl
import socket

from forwarder import Forwarder


def handle_connection(client_socket: ssl.SSLSocket, client: tuple[str, int], modification_params):
    with client_socket:
        try:
            data = client_socket.recv(6)
            server_address = socket.inet_ntoa(data[:4])
            server_port = int.from_bytes(data[4:6], byteorder='big', signed=False)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((server_address, server_port))
                try:
                    client_socket.send(b'OK')
                except Exception as e:
                    print(f"Failed to send confirmation to client. Error message: {e}")
                print(f"Tunneling data between {client} and {(server_address, server_port)}")
                Forwarder(client_socket, server_socket, modification_params).run()
                print(f"Connection between {client} and {(server_address, server_port)} closed.")
        except Exception as e:
            print(f"Failed to connect to the server. Error message: {e}")
            try:
                client_socket.send(b'NO')
            except Exception as e:
                print(f"Failed to send 'server unavailable' message to client. Error message: {e}")


def add_connection(client_socket: ssl.SSLSocket, client: tuple[str, int], modification_params):
    Thread(
        target=handle_connection,
        args=(client_socket, client, modification_params),
        daemon=True,
    ).start()
