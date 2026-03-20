"""
Memory struct_example9
struct_example9
"""
import struct


def demo():
    data = struct.pack("ci", b"x", 42)
    unpacked = struct.unpack("ci", data)
    print(unpacked)


if __name__ == "__main__":
    demo()
