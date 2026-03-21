"""
Memory hashlib_example21
hashlib_example21
"""
import hashlib


def demo():
    h = hashlib.blake2s(b"data")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
