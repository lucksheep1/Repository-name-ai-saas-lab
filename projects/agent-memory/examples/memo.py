"""
Memory Memo
Memoization
"""
from memory import Memory


def memo(func):
    cache = {}
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


@memo
def cached_add(x, y):
    return x + y


def demo():
    print(cached_add(1, 2))


if __name__ == "__main__":
    demo()
