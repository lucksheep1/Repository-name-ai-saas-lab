"""
Memory struct_example2
struct_example2
"""
import struct


def demo():
    data = struct.pack("3i", 1, 2, 3)
    a, b, c = struct.unpack("3i", data)
    print(a, b, c)


if __name__ == "__main__":
    demo()
