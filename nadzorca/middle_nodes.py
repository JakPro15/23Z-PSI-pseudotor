from threading import Lock
from time import time


class MiddleNodes:
    def __init__(self, timeout: float, cleaning_interval: float):
        self.mutex = Lock()
        self.middleNodesIps = {}
        self.timeout = timeout
        self.last_cleaning = time()
        self.cleaning_interval = cleaning_interval

    def add_node(self, nodeIpAddress: str):
        with self.mutex:
            self.middleNodesIps[nodeIpAddress] = time()

    def _clean_expired(self):
        now = time()
        if now - self.last_cleaning < self.cleaning_interval:
            return
        to_remove = []
        for ip_address, last_registration in self.middleNodesIps.items():
            if now - last_registration > self.timeout:
                to_remove.append(ip_address)
        for ip_address in to_remove:
            del self.middleNodesIps[ip_address]
        self.last_cleaning = now

    def get_nodes(self) -> list[str]:
        with self.mutex:
            self._clean_expired()
            return [ip_address for ip_address in self.middleNodesIps.keys()]


middle_nodes = MiddleNodes()
