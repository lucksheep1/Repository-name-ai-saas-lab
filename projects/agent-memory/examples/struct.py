"""
Memory struct
struct utilities
"""
import struct


def demo():
    packed = struct.pack("i", 42)
    print(struct.unpack("i", packed))


if __name__ == "__main__":
    demo()
