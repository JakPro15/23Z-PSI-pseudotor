from typing import Tuple


class TrafficModifier:
    def __init__(
        self,
        max_delay: float,
        output_segmentation_range: Tuple[int, int] | None,
    ):
        self.max_delay = max_delay
        self.segmentation_range = output_segmentation_range
        self.buffer = bytearray()

    def segment_data(self, data):
        ...

    def desegment_data(self):
        ...
