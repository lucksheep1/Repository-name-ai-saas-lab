"""
Memory secrets_example3
secrets_example3
"""
import secrets


def demo():
    print(secrets.compare_digest(b"abc", b"abc"))


if __name__ == "__main__":
    demo()
