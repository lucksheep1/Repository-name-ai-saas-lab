"""
Memory secrets_example19
secrets_example19
"""
import secrets


def demo():
    print(secrets.compare_digest(b"a", b"a"))


if __name__ == "__main__":
    demo()
