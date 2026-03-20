"""
Memory functools_example15
functools_example15
"""
from functools import singledispatch


@singledispatch
def process(arg):
    return str(arg)


@process.register(int)
def process_int(arg):
    return f"int: {arg}"


def demo():
    print(process("hello"))
    print(process(42))


if __name__ == "__main__":
    demo()
