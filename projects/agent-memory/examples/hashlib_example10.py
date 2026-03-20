"""
Memory hashlib_example10
hashlib_example10
"""
import hashlib


def demo():
    print(hashlib.sha512(b"test").hexdigest())


if __name__ == "__main__":
    demo()
