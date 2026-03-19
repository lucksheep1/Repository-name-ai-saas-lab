"""
Memory secrets_example6
secrets_example6
"""
import secrets


def demo():
    token = secrets.token_urlsafe(16)
    print(token)


if __name__ == "__main__":
    demo()
