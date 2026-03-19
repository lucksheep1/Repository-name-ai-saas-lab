"""
Memory HMAC
HMAC utilities
"""
from memory import Memory
import hmac


def demo():
    h = hmac.new(b"key", b"message", digestmod="sha256")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
