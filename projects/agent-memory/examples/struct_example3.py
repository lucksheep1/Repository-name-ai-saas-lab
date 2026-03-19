"""
Memory struct_example3
struct_example3
"""
import struct


def demo():
    packed = struct.pack("ff", 3.14, 2.71)
    a, b = struct.unpack("ff", packed)
    print(a, b)


if __name__ == "__main__":
    demo()
