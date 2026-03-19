"""
Memory contextlib
contextlib utilities
"""
from memory import Memory
from contextlib import contextmanager


@contextmanager
def my_context():
    print("enter")
    yield
    print("exit")


def demo():
    with my_context():
        print("inside")


if __name__ == "__main__":
    demo()
