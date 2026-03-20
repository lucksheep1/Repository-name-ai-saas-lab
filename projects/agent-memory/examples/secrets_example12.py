"""
Memory secrets_example12
secrets_example12
"""
import secrets


def demo():
    print(secrets.compare_digest("abc", "abc"))
    print(secrets.compare_digest("abc", "def"))


if __name__ == "__main__":
    demo()
