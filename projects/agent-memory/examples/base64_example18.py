"""
Memory base64_example18
base64_example18
"""
import base64


def demo():
    data = b"hello world"
    print(base64.urlsafe_b64encode(data).decode())


if __name__ == "__main__":
    demo()
