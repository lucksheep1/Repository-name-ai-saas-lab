"""
Memory Hashlib
Hashing utilities
"""
from memory import Memory
import hashlib


def demo():
    h = hashlib.sha256(b"test")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
