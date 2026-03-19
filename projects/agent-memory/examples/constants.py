"""
Memory Constants
Constants
"""
from memory import Memory


class Constants:
    DEFAULT_STORAGE = "json"
    DEFAULT_PATH = "memory.json"
    MAX_CONTENT_LENGTH = 10000


def demo():
    print(Constants.DEFAULT_STORAGE)


if __name__ == "__main__":
    demo()
