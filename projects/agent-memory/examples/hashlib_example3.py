"""
Memory hashlib_example3
hashlib_example3
"""
import hashlib


def demo():
    md5 = hashlib.md5()
    md5.update(b"hello")
    print(md5.hexdigest())


if __name__ == "__main__":
    demo()
