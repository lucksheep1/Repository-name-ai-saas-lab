"""
Memory Wrap
Wrapper function
"""
from memory import Memory


def wrapper(func):
    def inner(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return inner


@wrapper
def wrapped():
    print("Inside")


def demo():
    wrapped()


if __name__ == "__main__":
    demo()
