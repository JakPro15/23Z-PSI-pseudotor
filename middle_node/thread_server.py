from threading import Thread
from typing import Dict


class ConnectionServer:
    def __init__(self):
        self.threads: Dict[str, Thread] = {}

    def add_connection(self, address: str):
        ...

    def remove_connection(self, address: str):
        ...
