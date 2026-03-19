"""
Memory secrets
secrets utilities
"""
import secrets


def demo():
    print(secrets.token_hex(16))


if __name__ == "__main__":
    demo()
