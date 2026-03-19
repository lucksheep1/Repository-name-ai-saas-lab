"""
Memory Compose
Function composition
"""
from memory import Memory


def compose(*funcs):
    def composed(x):
        result = x
        for func in reversed(funcs):
            result = func(result)
        return result
    return composed


def add_one(x):
    return x + 1


def double(x):
    return x * 2


def demo():
    f = compose(double, add_one)
    print(f(5))


if __name__ == "__main__":
    demo()
