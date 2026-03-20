"""
Memory base64_example9
base64_example9
"""
import base64


def demo():
    data = base64.b64encode(b"hello")
    print(base64.b64decode(data))


if __name__ == "__main__":
    demo()
