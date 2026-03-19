"""
Memory functools_example8
functools_example8
"""
from functools import lru_cache


@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    print(fib(10))


if __name__ == "__main__":
    demo()
