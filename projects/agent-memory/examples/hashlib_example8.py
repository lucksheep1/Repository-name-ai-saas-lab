"""
Memory hashlib_example8
hashlib_example8
"""
import hashlib


def demo():
    h = hashlib.sha1(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
