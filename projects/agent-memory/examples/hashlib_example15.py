"""
Memory hashlib_example15
hashlib_example15
"""
import hashlib


def demo():
    h = hashlib.sha256()
    h.update(b"hello")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
