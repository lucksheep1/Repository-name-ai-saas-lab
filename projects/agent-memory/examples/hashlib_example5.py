"""
Memory hashlib_example5
hashlib_example5
"""
import hashlib


def demo():
    h = hashlib.blake2b(digest_size=16)
    h.update(b"data")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
