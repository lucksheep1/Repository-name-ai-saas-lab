"""
Memory hashlib
hashlib utilities
"""
import hashlib


def demo():
    h = hashlib.sha256(b"test")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
