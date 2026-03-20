"""
Memory hashlib_example16
hashlib_example16
"""
import hashlib


def demo():
    h = hashlib.sha512(b"data")
    print(h.hexdigest()[:32])


if __name__ == "__main__":
    demo()
