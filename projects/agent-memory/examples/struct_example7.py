"""
Memory struct_example7
struct_example7
"""
import struct


def demo():
    data = struct.pack("?", True)
    unpacked = struct.unpack("?", data)
    print(unpacked)


if __name__ == "__main__":
    demo()
