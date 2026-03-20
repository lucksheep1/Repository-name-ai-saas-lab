"""
Memory base64_example13
base64_example13
"""
import base64


def demo():
    print(base64.urlsafe_b64encode(b"hello").decode())


if __name__ == "__main__":
    demo()
