"""
Memory base64_example5
base64_example5
"""
import base64


def demo():
    s = b"hello world"
    encoded = base64.b64encode(s)
    print(encoded)


if __name__ == "__main__":
    demo()
