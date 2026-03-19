"""
Memory base64_example6
base64_example6
"""
import base64


def demo():
    s = b"test"
    encoded = base64.urlsafe_b64encode(s)
    print(encoded)


if __name__ == "__main__":
    demo()
