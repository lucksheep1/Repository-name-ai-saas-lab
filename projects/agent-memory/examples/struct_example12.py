"""
Memory struct_example12
struct_example12
"""
import struct


def demo():
    data = struct.pack("f", 3.14)
    print(struct.unpack("f", data)[0])


if __name__ == "__main__":
    demo()
