"""
Memory secrets_example16
secrets_example16
"""
import secrets


def demo():
    token = secrets.token_bytes(16)
    print(len(token))


if __name__ == "__main__":
    demo()
