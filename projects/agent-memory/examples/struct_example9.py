"""
Memory struct_example9
struct_example9
"""
import struct


def demo():
    data = struct.pack("cii", 1, b"ab", 3)
    print(len(data))


if __name__ == "__main__":
    demo()
