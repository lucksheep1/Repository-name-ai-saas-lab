"""
Memory struct_example6
struct_example6
"""
import struct


def demo():
    data = struct.pack("f", 3.14)
    unpacked = struct.unpack("f", data)
    print(unpacked)


if __name__ == "__main__":
    demo()
