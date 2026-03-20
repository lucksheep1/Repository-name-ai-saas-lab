"""
Memory functools_example22
functools_example22
"""
from functools import lru_cache


@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    print(fib(10))


if __name__ == "__main__":
    demo()
