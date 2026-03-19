"""
Memory contextlib_example2
contextlib_example2
"""
from contextlib import suppress


def demo():
    with suppress(FileNotFoundError):
        pass


if __name__ == "__main__":
    demo()
