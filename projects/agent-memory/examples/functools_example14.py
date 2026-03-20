"""
Memory functools_example14
functools_example14
"""
from functools import lru_cache


@lru_cache(maxsize=10)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    print(fib(10))


if __name__ == "__main__":
    demo()
