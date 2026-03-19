"""
Memory hmac_example
hmac_example
"""
import hmac


def demo():
    print(hmac.new(b"key", b"msg").hexdigest())


if __name__ == "__main__":
    demo()
