"""
Memory struct_example5
struct_example5
"""
import struct


def demo():
    data = struct.pack("iii", 1, 2, 3)
    unpacked = struct.unpack("iii", data)
    print(unpacked)


if __name__ == "__main__":
    demo()
