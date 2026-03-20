"""
Memory hashlib_example13
hashlib_example13
"""
import hashlib


def demo():
    h = hashlib.md5(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
