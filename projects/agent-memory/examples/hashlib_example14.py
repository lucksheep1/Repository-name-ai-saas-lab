"""
Memory hashlib_example14
hashlib_example14
"""
import hashlib


def demo():
    h = hashlib.sha1(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
