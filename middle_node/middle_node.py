import random
from typing import Tuple


class MiddleNode:
    def __init__(
        self,
        max_delay: float,
        new_segmentation_range: Tuple[int, int] | None,
    ):
        self.max_delay = max_delay
        self.segmentation_range = new_segmentation_range
        pass

    # def register(self, )
