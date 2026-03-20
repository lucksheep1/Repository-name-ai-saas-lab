"""
Memory weakref_example5
weakref_example5
"""
import weakref


class A:
    def __init__(self, value):
        self.value = value


def demo():
    a = A(42)
    ref = weakref.ref(a)
    print(ref().value)


if __name__ == "__main__":
    demo()
