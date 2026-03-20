"""
Memory contextlib_example14
contextlib_example14
"""
from contextlib import suppress


def demo():
    with suppress(FileNotFoundError):
        open("/nonexistent/file.txt").read()


if __name__ == "__main__":
    demo()
