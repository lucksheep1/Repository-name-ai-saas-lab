"""
Memory functools_example4
functools_example4
"""
from functools import wraps


def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


@my_decorator
def example():
    pass


def demo():
    print(example.__name__)


if __name__ == "__main__":
    demo()
