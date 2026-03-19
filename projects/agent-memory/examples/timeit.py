"""
Memory Timeit
Timing decorator
"""
from memory import Memory


def timeit(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return result
    return wrapper


@timeit
def timed_func():
    return sum(range(1000))


def demo():
    timed_func()


if __name__ == "__main__":
    demo()
