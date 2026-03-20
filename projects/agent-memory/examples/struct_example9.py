"""
Memory struct_example9
struct_example9
"""
import struct


def demo():
    data = struct.pack("ccc", b"a", b"b", b"c")
    print(struct.unpack("ccc", data))


if __name__ == "__main__":
    demo()
