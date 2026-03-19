"""
Memory secrets_example4
secrets_example4
"""
import secrets


def demo():
    token = secrets.token_urlsafe(32)
    print(token[:16])


if __name__ == "__main__":
    demo()
