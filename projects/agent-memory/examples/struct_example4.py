"""
Memory struct_example4
struct_example4
"""
import struct


def demo():
    packed = struct.pack("ci", b"x", 42)
    print(struct.unpack("ci", packed))


if __name__ == "__main__":
    demo()
