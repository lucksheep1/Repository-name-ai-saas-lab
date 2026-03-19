"""
Memory Cache Decorator
Cache decorator
"""
from memory import Memory
from functools import wraps


def cached(cache={}):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator


@cached()
def expensive_func(x):
    return x * 2


def demo():
    print(expensive_func(5))


if __name__ == "__main__":
    demo()
