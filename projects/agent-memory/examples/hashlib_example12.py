"""
Memory hashlib_example12
hashlib_example12
"""
import hashlib


def demo():
    h = hashlib.sha256(b"test")
    print(h.hexdigest()[:16])


if __name__ == "__main__":
    demo()
