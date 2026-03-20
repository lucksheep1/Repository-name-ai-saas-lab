"""
Memory contextlib_example11
contextlib_example11
"""
from contextlib import contextmanager


@contextmanager
def my_context():
    yield "value"


def demo():
    with my_context() as v:
        print(v)


if __name__ == "__main__":
    demo()
