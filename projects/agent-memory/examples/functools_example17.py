"""
Memory functools_example17
functools_example17
"""
from functools import lru_cache


@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    print(fib(30))
    print(fib.cache_info())


if __name__ == "__main__":
    demo()
