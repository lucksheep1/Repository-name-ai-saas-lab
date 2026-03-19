"""
Memory hmac
hmac utilities
"""
import hmac


def demo():
    h = hmac.new(b"key", b"msg", digestmod="sha256")
    print(h.hexdigest())


if __name__ == "__main__":
    demo()
