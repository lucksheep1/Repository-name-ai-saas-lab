"""
Memory contextlib_example4
contextlib_example4
"""
from contextlib import ExitStack


def demo():
    with ExitStack() as stack:
        print("cleanup handled")


if __name__ == "__main__":
    demo()
