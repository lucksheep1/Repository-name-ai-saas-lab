"""
Memory hmac_example2
hmac_example2
"""
import hmac


def demo():
    result = hmac.new(b"key", b"message", "sha256").hexdigest()
    print(result)


if __name__ == "__main__":
    demo()
