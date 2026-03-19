"""
Memory Curry
Currying
"""
from memory import Memory


def curry(func, arity=None):
    if arity is None:
        arity = func.__code__.co_argcount
    
    def curried(*args):
        if len(args) >= arity:
            return func(*args)
        return lambda *rest: curried(*(args + rest))
    return curried


def add(a, b, c):
    return a + b + c


curried_add = curry(add)


def demo():
    print(curried_add(1)(2)(3))


if __name__ == "__main__":
    demo()
