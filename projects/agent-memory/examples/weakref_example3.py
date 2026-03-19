"""
Memory weakref_example3
weakref_example3
"""
import weakref


class Foo:
    def __init__(self, name):
        self.name = name


def demo():
    obj = Foo("test")
    ref = weakref.ref(obj)
    print(ref().name)


if __name__ == "__main__":
    demo()
