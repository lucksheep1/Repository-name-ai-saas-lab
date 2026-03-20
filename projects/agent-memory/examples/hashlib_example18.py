"""
Memory hashlib_example18
hashlib_example18
"""
import hashlib


def demo():
    h = hashlib.sha1(b"test")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
