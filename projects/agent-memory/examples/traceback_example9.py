"""
Memory traceback_example9
traceback_example9
"""
import traceback
import sys


def inner():
    raise ValueError("Test error")


def outer():
    inner()


def demo():
    try:
        outer()
    except ValueError:
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    demo()
