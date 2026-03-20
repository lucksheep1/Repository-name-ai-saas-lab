"""
Memory secrets_example18
secrets_example18
"""
import secrets


def demo():
    print(secrets.token_urlsafe(16))


if __name__ == "__main__":
    demo()
