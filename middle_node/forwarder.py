import socket
import time
from threading import Thread


BUFFER_TIMEOUT = 0.2
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
        except Exception:
            print(f"{name}: Error")
            return
        else:
            if data == b'':
                print(f"{name}: Shutdown")
                break
            print(f"{name}: Appending")
            to_send.extend(data)
            if len(to_send) > BUFFER_SIZE_THRESHOLD:
                print(f"{name}: Sending")
                # TUTAJ MA BYĆ PROPER SEGMENTACJA, NAJLEPIEJ W FUNKCJI ODDZIELNEJ
                for i in range(20):
                    to_socket.sendall(to_send[100 * i:100 * (i + 1)])
                    time.sleep(0.5)
                to_send = bytearray()
    if len(to_send) > 0:
        print(f"{name}: Sending {to_send}")
        to_socket.sendall(to_send)
    forwarder.stop = True
    print(f"{name}: End")


HOST = 'localhost'
PORT = 5555
SERVER = 'localhost'
SERVER_PORT = 8000
if __name__ == '__main__':
     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind((HOST, PORT))
        listening_socket.listen(5)
        print(f"Waiting for data on address {(HOST, PORT)}")
        while True:
            conn, addr = listening_socket.accept()
            with conn:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connecting_socket:
                    connecting_socket.connect((SERVER, SERVER_PORT))
                    Forwarder(conn, connecting_socket).run()
