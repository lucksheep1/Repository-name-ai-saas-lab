"""
Memory NoReturn
NoReturn type
"""
from memory import Memory
from typing import NoReturn


def fatal_error() -> NoReturn:
    raise Exception("Fatal error")


def demo():
    try:
        fatal_error()
    except Exception as e:
        print(f"Caught: {e}")


if __name__ == "__main__":
    demo()
