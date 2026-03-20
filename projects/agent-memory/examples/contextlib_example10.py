"""
Memory contextlib_example10
contextlib_example10
"""
from contextlib import ExitStack


def demo():
    with ExitStack() as stack:
        print("exited")


if __name__ == "__main__":
    demo()
