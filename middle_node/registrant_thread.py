import socket
from threading import Thread
from time import sleep
from typing import Tuple


class RegistrantThread(Thread):
    def __init__(self, address: Tuple[str, int], timeout: float):
        self.address = address
        self.timeout = timeout
        super(RegistrantThread, self).__init__(daemon=True)

    def run(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(self.address)
                sock.send(b"PSEUDOTOR_REGISTER")
            sleep(self.timeout)
