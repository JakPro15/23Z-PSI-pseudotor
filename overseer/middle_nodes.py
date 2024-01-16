from threading import Lock
from time import time


class MiddleNodes:
    def __init__(self, timeout: float):
        self.mutex = Lock()
        self.middleNodesIps = {}
        self.timeout = timeout

    def add_node(self, nodeIpAddress: str):
        with self.mutex:
            try:
                self.middleNodesIps[nodeIpAddress] = time()
            except Exception as e:
                print(f"Error adding node: {e}")

    def _clean_expired(self):
        try:
            now = time()
            to_remove = []
            for ip_address, last_registration in self.middleNodesIps.items():
                if now - last_registration > self.timeout:
                    to_remove.append(ip_address)
            for ip_address in to_remove:
                del self.middleNodesIps[ip_address]
            self.last_cleaning = now
        except Exception as e:
            print(f"Error cleaning expired nodes: {e}")

    def get_nodes(self) -> list[str]:
        with self.mutex:
            try:
                self._clean_expired()
                return [ip_address for ip_address in self.middleNodesIps.keys()]
            except Exception as e:
                print(f"Error getting nodes: {e}")


middle_nodes = MiddleNodes(5 * 60)
