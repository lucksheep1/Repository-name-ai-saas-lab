"""
Memory secrets_example14
secrets_example14
"""
import secrets


def demo():
    token = secrets.token_hex(16)
    print(len(token))


if __name__ == "__main__":
    demo()
