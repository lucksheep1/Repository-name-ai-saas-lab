"""
Memory secrets_example11
secrets_example11
"""
import secrets


def demo():
    token = secrets.token_urlsafe(32)
    print(len(token))


if __name__ == "__main__":
    demo()
