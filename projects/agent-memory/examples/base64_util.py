"""
Memory base64
base64 utilities
"""
import base64


def demo():
    encoded = base64.b64encode(b"hello")
    print(encoded)


if __name__ == "__main__":
    demo()
