"""
Memory hashlib_example20
hashlib_example20
"""
import hashlib


def demo():
    h = hashlib.sha256(b"data")
    print(h.digest_size)


if __name__ == "__main__":
    demo()
