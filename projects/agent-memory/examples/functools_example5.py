"""
Memory functools_example5
functools_example5
"""
from functools import singledispatch


@singledispatch
def process(arg):
    print(f"Object: {arg}")


@process.register(int)
def process_int(arg):
    print(f"Integer: {arg}")


def demo():
    process("hello")
    process(42)


if __name__ == "__main__":
    demo()
