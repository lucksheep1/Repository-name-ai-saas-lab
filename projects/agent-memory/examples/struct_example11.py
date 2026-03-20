"""
Memory struct_example11
struct_example11
"""
import struct


def demo():
    data = struct.pack("i", 42)
    print(struct.unpack("i", data)[0])


if __name__ == "__main__":
    demo()
