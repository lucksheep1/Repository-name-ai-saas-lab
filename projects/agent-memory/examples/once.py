"""
Memory Once
Run once decorator
"""
from memory import Memory


def once(func):
    called = [False]
    result = [None]
    def wrapper(*args, **kwargs):
        if not called[0]:
            called[0] = True
            result[0] = func(*args, **kwargs)
        return result[0]
    return wrapper


@once
def once_func():
    return "Called once"


def demo():
    print(once_func())
    print(once_func())


if __name__ == "__main__":
    demo()
