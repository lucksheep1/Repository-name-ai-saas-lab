"""
Memory hashlib_example
hashlib_example
"""
import hashlib


def demo():
    print(hashlib.md5(b"test").hexdigest())


if __name__ == "__main__":
    demo()
