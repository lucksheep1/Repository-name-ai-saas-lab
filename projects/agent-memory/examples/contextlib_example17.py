"""
Memory contextlib_example17
contextlib_example17
"""
from contextlib import suppress


def demo():
    with suppress(FileNotFoundError, PermissionError):
        open("/nonexistent").read()


if __name__ == "__main__":
    demo()
