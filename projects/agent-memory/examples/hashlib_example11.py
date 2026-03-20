"""
Memory hashlib_example11
hashlib_example11
"""
import hashlib


def demo():
    data = b"test data"
    h = hashlib.blake2b(data)
    print(h.hexdigest()[:16])


if __name__ == "__main__":
    demo()
