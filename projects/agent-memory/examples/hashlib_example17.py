"""
Memory hashlib_example17
hashlib_example17
"""
import hashlib


def demo():
    h = hashlib.md5(b"data")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
