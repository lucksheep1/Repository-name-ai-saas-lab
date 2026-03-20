"""
Memory secrets_example9
secrets_example9
"""
import secrets


def demo():
    print(secrets.token_bytes(16))


if __name__ == "__main__":
    demo()
