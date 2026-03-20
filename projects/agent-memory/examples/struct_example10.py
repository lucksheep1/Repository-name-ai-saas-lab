"""
Memory struct_example10
struct_example10
"""
import struct


def demo():
    packed = struct.pack("I", 42)
    print(struct.unpack("I", packed))


if __name__ == "__main__":
    demo()
