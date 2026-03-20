"""
Memory base64_example11
base64_example11
"""
import base64


def demo():
    print(base64.b16encode(b"hello").decode())


if __name__ == "__main__":
    demo()
