"""
Memory Throttle
Throttle operations
"""
from memory import Memory
import time


def throttle(interval):
    last_called = [0]
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            if now - last_called[0] >= interval:
                last_called[0] = now
                return func(*args, **kwargs)
        return wrapper
    return decorator


@throttle(1)
def throttled_func():
    print("Called")


def demo():
    throttled_func()
    throttled_func()


if __name__ == "__main__":
    demo()
