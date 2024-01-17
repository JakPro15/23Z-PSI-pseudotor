import socket
from threading import Thread
from time import sleep


class RegistrantThread(Thread):
    def __init__(self, overseer_address: str, timeout: float):
        self.overseer = (overseer_address, 8001)
        self.timeout = timeout
        super(RegistrantThread, self).__init__(daemon=True)

    def run(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(self.overseer)
                    sock.send(b"PSEUDOTOR_REGISTER")
            except Exception as e:
                print(f"Failed to register to overseer. Error message: {e}")
            sleep(self.timeout)
