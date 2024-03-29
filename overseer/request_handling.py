import middle_nodes
import socket


def handle_request(conn: socket.socket, addr: tuple, buffer_size: int):
    with conn:
        try:
            data = conn.recv(buffer_size)
        except Exception as e:
            print(f"Exception encountered while receiving request. Error message: {e}")

        if data == b"PSEUDOTOR_REGISTER":
            do_registration(addr)
        elif data == b"PSEUDOTOR_GET_NODES":
            do_list_sharing(conn)
        else:
            print("Invalid request for the overseer service.")


def do_registration(addr: tuple):
    try:
        middle_nodes.middle_nodes.add_node(addr[0])
        print(f"Registered {addr[0]} as middle node")
    except Exception as e:
        print(f"Error during registration of {addr[0]}. Error message: {e}")


def serialize_middlenodes_list(middle_nodes_list: list[str]) -> bytes:
    result = b''
    for ip_address in middle_nodes_list:
        result += ip_address.encode('ascii')
        result += b' '
    return result


def do_list_sharing(conn: socket.socket):
    try:
        nodes = middle_nodes.middle_nodes.get_nodes()
        print(f"Sending middle nodes list of length {len(nodes)}")
        conn.send(serialize_middlenodes_list(nodes))
    except Exception as e:
        print(f"Exception encountered while sending middle nodes list. Error message: {e}")
