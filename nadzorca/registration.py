import socket
import middle_nodes


def registration_thread(ip_address: str, buffer_size: int, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind((ip_address, port))
        listening_socket.listen(5)
        print("Waiting for requests")
        while True:
            conn, addr = listening_socket.accept()
            print(f"Connected to {addr[0]}:{addr[1]}")
            with conn:
                data = conn.recv(buffer_size)
                try:
                    if data.decode('ascii') != "PSEUDOTOR_REGISTER":
                        raise ValueError('Invalid request for this service.')
                except Exception:
                    print("Invalid request received. Ignoring")
                    continue
                middle_nodes.middle_nodes.add_node(addr[0])
            conn.close()
