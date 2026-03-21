"""
Memory hashlib_example19
hashlib_example19
"""
import hashlib


def demo():
    h = hashlib.blake2b(b"data")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
