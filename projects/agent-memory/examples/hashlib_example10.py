"""
Memory hashlib_example10
hashlib_example10
"""
import hashlib


def demo():
    h = hashlib.sha512(b"test")
    print(h.hexdigest()[:16])


if __name__ == "__main__":
    demo()
