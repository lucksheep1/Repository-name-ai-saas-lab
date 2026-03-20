"""
Memory base64_example12
base64_example12
"""
import base64


def demo():
    print(base64.b32encode(b"hello").decode())


if __name__ == "__main__":
    demo()
