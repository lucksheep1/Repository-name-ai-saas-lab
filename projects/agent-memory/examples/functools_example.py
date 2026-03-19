"""
Memory functools_example
functools_example
"""
from functools import lru_cache


@lru_cache()
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)


def demo():
    print(fib(10))


if __name__ == "__main__":
    demo()
