import socket
import middle_nodes


def serialize_middlenodes_list(middle_nodes_list: list[str]) -> bytes:
    result = b''
    for ip_address in middle_nodes_list:
        result += ip_address.encode('ascii')
        result += b' '
    return result


def list_sharing_thread(ip_address: str, buffer_size: int, port: int):
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
                    if data.decode('ascii') != "PSEUDOTOR_GET_NODES":
                        raise ValueError('Invalid request for this service.')
                except Exception:
                    print("Invalid request received. Ignoring")
                    continue
                nodes = middle_nodes.middle_nodes.get_nodes()
                conn.send(serialize_middlenodes_list(nodes))
            conn.close()
