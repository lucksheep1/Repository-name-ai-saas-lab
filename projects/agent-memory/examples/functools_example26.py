"""
Memory functools_example26
functools_example26
"""
from functools import singledispatch


@singledispatch
def process(arg):
    print(f"Object: {arg}")


@process.register(int)
def _(arg):
    print(f"Integer: {arg * 2}")


def demo():
    process(10)
    process("hello")


if __name__ == "__main__":
    demo()
