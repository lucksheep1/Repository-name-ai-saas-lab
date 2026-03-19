"""
Memory weakref
weakref utilities
"""
from memory import Memory
import weakref


class Foo:
    pass


def demo():
    obj = Foo()
    ref = weakref.ref(obj)
    print(ref() is obj)


if __name__ == "__main__":
    demo()
