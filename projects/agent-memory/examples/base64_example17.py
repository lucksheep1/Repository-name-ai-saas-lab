"""
Memory base64_example17
base64_example17
"""
import base64


def demo():
    print(base64.b64decode(b"aGVsbG8=").decode())


if __name__ == "__main__":
    demo()
