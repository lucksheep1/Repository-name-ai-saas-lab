"""
Memory contextlib_example
contextlib_example
"""
from contextlib import contextmanager


@contextmanager
def my_context():
    yield


def demo():
    with my_context():
        pass


if __name__ == "__main__":
    demo()
