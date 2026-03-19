"""
Memory hashlib_example4
hashlib_example4
"""
import hashlib


def demo():
    h = hashlib.sha384(b"test")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
