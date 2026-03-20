"""
Memory base64_example10
base64_example10
"""
import base64


def demo():
    data = b"Hello World"
    encoded = base64.b64encode(data)
    decoded = base64.b64decode(encoded)
    print(decoded)


if __name__ == "__main__":
    demo()
