import socket
from random import randint, uniform
from time import sleep


def segment_data(data: bytearray, seg_min: int, seg_max: int) -> list[bytearray]:
    slices = []
    position = 0
    seg_size = randint(seg_min, seg_max)

    while(position + seg_size <= len(data)):
        slices.append(data[position: position + seg_size])
        position += seg_size
        seg_size = randint(seg_min, seg_max)
    slices.append(data[position:])

    return slices


def send_segmented(to_socket: socket.socket, to_send: bytearray, modification_params, all: bool):
    try:
        if modification_params[1] is not None:
            for slice in segment_data(to_send, modification_params[1][0], modification_params[1][1]):
                if not all and len(slice) < modification_params[1][0]:
                    return slice
                sleep(uniform(0, modification_params[0]))
                to_socket.sendall(slice)
        else:
            sleep(uniform(0, modification_params[0]))
            to_socket.sendall(to_send)
    except Exception as e:
        print(f"Exception encountered when sending segmented data. Error message: {e}")
        raise
    return bytearray()
