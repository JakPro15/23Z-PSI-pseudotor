import socket
from threading import Thread

from packet_modifying import send_segmented


MAX_DATA_GATHERING_TIME = 0.05
CHECKING_FOR_STOP_TIMEOUT = 0.5
BUFFER_SIZE_THRESHOLD = 2000


class Forwarder:
    def __init__(self, client_socket: socket.socket, server_socket: socket.socket, modification_params):
        self.stop = False
        self.client_socket = client_socket
        self.server_socket = server_socket
        self.modification_params = modification_params

    def run(self):
        try:
            client_to_server = Thread(
                None, forward, None,
                (self, self.client_socket, self.server_socket, self.modification_params, "client_to_server")
            )
            server_to_client = Thread(
                None, forward, None,
                (self, self.server_socket, self.client_socket, self.modification_params, "server_to_client")
            )
            client_to_server.start()
            server_to_client.start()
            client_to_server.join()
            server_to_client.join()
            self.client_socket.close()
            self.server_socket.close()
        except Exception as e:
            print(f"An unexpected error occurred in Forwarder: {e}")


def forward(forwarder: Forwarder, from_socket: socket.socket, to_socket: socket.socket, modification_params, name: str):
    to_send = bytearray()
    from_socket.settimeout(MAX_DATA_GATHERING_TIME)
    try:
        while not forwarder.stop:
            try:
                data = from_socket.recv(1024)
            except TimeoutError:
                if len(to_send) > 0:
                    send_segmented(to_socket, to_send, modification_params)
                    to_send = bytearray()
                from_socket.settimeout(CHECKING_FOR_STOP_TIMEOUT)
            except Exception as e:
                print(f"Exception encountered in {name} thread: {e}")
                return
            else:
                if data == b'':
                    break
                if len(to_send) == 0:
                    from_socket.settimeout(MAX_DATA_GATHERING_TIME)
                to_send.extend(data)
                if len(to_send) > BUFFER_SIZE_THRESHOLD:
                    send_segmented(to_socket, to_send, modification_params)
                    to_send = bytearray()
                    from_socket.settimeout(CHECKING_FOR_STOP_TIMEOUT)
        if len(to_send) > 0:
            send_segmented(to_socket, to_send, modification_params)
    except Exception as e:
        print(f"An unexpected error occurred in {name} thread: {e}")
    finally:
        forwarder.stop = True
