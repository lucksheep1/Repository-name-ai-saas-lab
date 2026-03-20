"""
Memory functools_example16
functools_example16
"""
from functools import cache


@cache
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    print(fib(20))
    print(fib(25))


if __name__ == "__main__":
    demo()
