"""
Memory hashlib_example9
hashlib_example9
"""
import hashlib


def demo():
    print(hashlib.sha256(b"test").hexdigest())


if __name__ == "__main__":
    demo()
