"""
Memory weakref_example7
weakref_example7
"""
import weakref


class A:
    pass


def demo():
    a = A()
    ref = weakref.ref(a)
    print(ref() is a)


if __name__ == "__main__":
    demo()
