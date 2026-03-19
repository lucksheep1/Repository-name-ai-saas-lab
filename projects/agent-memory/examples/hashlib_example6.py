"""
Memory hashlib_example6
hashlib_example6
"""
import hashlib


def demo():
    h = hashlib.sha256(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
