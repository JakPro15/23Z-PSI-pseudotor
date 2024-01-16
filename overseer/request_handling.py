import middle_nodes
import socket


def handle_request(conn: socket.socket, addr: tuple, buffer_size: int):
    with conn:
        data = conn.recv(buffer_size)
        try:
            data = data.decode(encoding='ascii')
        except UnicodeError:
            print("Invalid request for the overseer service.")

        if data == "PSEUDOTOR_REGISTER":
            do_registration(addr)
        elif data == "PSEUDOTOR_GET_NODES":
            do_list_sharing(conn)
        else:
            print("Invalid request for the overseer service.")
    print(f"Request from {addr} handled")


def do_registration(addr: tuple):
    middle_nodes.middle_nodes.add_node(addr[0])
    print(f"Registered {addr[0]} as middle node")


def serialize_middlenodes_list(middle_nodes_list: list[str]) -> bytes:
    result = b''
    for ip_address in middle_nodes_list:
        result += ip_address.encode('ascii')
        result += b' '
    return result


def do_list_sharing(conn: socket.socket):
    nodes = middle_nodes.middle_nodes.get_nodes()
    print(f"Sending {len(nodes)} nodes")
    conn.send(serialize_middlenodes_list(nodes))
