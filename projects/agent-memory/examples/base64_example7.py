"""
Memory base64_example7
base64_example7
"""
import base64


def demo():
    decoded = base64.b64decode(b"aGVsbG8=")
    print(decoded)


if __name__ == "__main__":
    demo()
