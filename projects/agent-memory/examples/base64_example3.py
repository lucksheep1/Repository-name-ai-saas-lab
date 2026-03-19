"""
Memory base64_example3
base64_example3
"""
import base64


def demo():
    data = b"hello world"
    encoded = base64.b64encode(data)
    decoded = base64.b64decode(encoded)
    print(decoded)


if __name__ == "__main__":
    demo()
