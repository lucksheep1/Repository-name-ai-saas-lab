"""
Memory base64_example15
base64_example15
"""
import base64


def demo():
    print(base64.b64decode(b"SGVsbG8=").decode())


if __name__ == "__main__":
    demo()
