"""
Memory hashlib_example7
hashlib_example7
"""
import hashlib


def demo():
    h = hashlib.md5(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
