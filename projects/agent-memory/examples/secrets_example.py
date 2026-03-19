"""
Memory secrets_example
secrets_example
"""
import secrets


def demo():
    print(secrets.token_hex(16))


if __name__ == "__main__":
    demo()
