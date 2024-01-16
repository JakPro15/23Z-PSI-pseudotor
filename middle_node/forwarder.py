import socket
import time
import ssl
from threading import Thread


BUFFER_TIMEOUT = 0.05
STOP_CHECKING_TIMEOUT = 0.5
BUFFER_SIZE_THRESHOLD = 2000


class Forwarder:
    def __init__(self, client_socket: socket.socket, server_socket: socket.socket):
        self.stop = False
        self.client_socket = client_socket
        self.server_socket = server_socket

    def run(self):
        client_to_server = Thread(None, forward, None, (self, self.client_socket, self.server_socket, "c_to_s"))
        server_to_client = Thread(None, forward, None, (self, self.server_socket, self.client_socket, "s_to_c"))
        client_to_server.start()
        server_to_client.start()
        client_to_server.join()
        server_to_client.join()
        self.client_socket.close()
        self.server_socket.close()
        print("Exit")


def forward(forwarder: Forwarder, from_socket: socket.socket, to_socket: socket.socket, name: str):
    print(f"{name}: forwarding")
    to_send = bytearray()
    from_socket.settimeout(BUFFER_TIMEOUT)
    while not forwarder.stop:
        try:
            data = from_socket.recv(1024)
            print(f"{name} Received: {data}")
        except TimeoutError:
            print(f"{name}: Timeout")
            if len(to_send) > 0:
                to_socket.send(to_send)
                to_send = bytearray()
            from_socket.settimeout(STOP_CHECKING_TIMEOUT)
        except Exception:
            print(f"{name}: Error")
            return
        else:
            if data == b'':
                print(f"{name}: Shutdown")
                break
            print(f"{name}: Appending")
            if len(to_send) == 0:
                from_socket.settimeout(BUFFER_TIMEOUT)
            to_send.extend(data)
            if len(to_send) > BUFFER_SIZE_THRESHOLD:
                print(f"{name}: Sending")
                # TUTAJ MA BYĆ PROPER SEGMENTACJA, NAJLEPIEJ W FUNKCJI ODDZIELNEJ
                to_socket.sendall(to_send)
                to_send = bytearray()
    if len(to_send) > 0:
        print(f"{name}: Sending {to_send}")
        to_socket.sendall(to_send)
    forwarder.stop = True
    print(f"{name}: End")
