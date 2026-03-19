"""
Memory weakref_example2
weakref_example2
"""
import weakref


class Foo:
    def __init__(self, value):
        self.value = value


def demo():
    obj = Foo(42)
    ref = weakref.ref(obj)
    print(ref().value)


if __name__ == "__main__":
    demo()
