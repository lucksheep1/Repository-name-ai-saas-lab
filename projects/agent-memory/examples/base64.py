"""
Memory Base64
Base64 encoding
"""
from memory import Memory
import base64


def demo():
    encoded = base64.b64encode(b"test")
    print(encoded)
    decoded = base64.b64decode(encoded)
    print(decoded)


if __name__ == "__main__":
    demo()
