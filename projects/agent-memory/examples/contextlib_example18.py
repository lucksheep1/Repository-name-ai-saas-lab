"""
Memory contextlib_example18
contextlib_example18
"""
from contextlib import contextmanager


@contextmanager
def demo_context():
    print("enter")
    yield
    print("exit")


def demo():
    with demo_context():
        print("inside")


if __name__ == "__main__":
    demo()
