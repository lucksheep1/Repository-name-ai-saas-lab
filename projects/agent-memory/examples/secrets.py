"""
Memory Secrets
Secrets utilities
"""
from memory import Memory
import secrets


def demo():
    token = secrets.token_hex(32)
    print(token)


if __name__ == "__main__":
    demo()
