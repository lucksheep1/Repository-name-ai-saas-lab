"""
Memory Debounce
Debounce operations
"""
from memory import Memory
import time


def debounce(wait):
    timer = [None]
    def decorator(func):
        def wrapper(*args, **kwargs):
            def call():
                return func(*args, **kwargs)
            timer[0] and timer[0].cancel()
            timer[0] = time.Threading.Timer(wait, call)
            timer[0].start()
        return wrapper
    return decorator


def demo():
    print("Debounce ready")


if __name__ == "__main__":
    demo()
