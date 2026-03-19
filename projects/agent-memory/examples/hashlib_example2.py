"""
Memory hashlib_example2
hashlib_example2
"""
import hashlib


def demo():
    md5 = hashlib.md5(b"test").hexdigest()
    sha256 = hashlib.sha256(b"test").hexdigest()
    print(md5, sha256)


if __name__ == "__main__":
    demo()
