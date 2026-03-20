"""
Memory secrets_example8
secrets_example8
"""
import secrets


def demo():
    print(secrets.compare_digest("a", "a"))


if __name__ == "__main__":
    demo()
