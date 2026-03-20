"""
Memory contextlib_example12
contextlib_example12
"""
from contextlib import ContextDecorator


class my_context(ContextDecorator):
    def __enter__(self):
        print("enter")
        return self
    
    def __exit__(self, *args):
        print("exit")


def demo():
    with my_context():
        print("inside")


if __name__ == "__main__":
    demo()
