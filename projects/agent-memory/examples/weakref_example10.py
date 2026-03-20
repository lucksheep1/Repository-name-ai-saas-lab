"""
Memory weakref_example10
weakref_example10
"""
import weakref


class MyClass:
    def __init__(self, value):
        self.value = value


def demo():
    obj = MyClass(100)
    ref = weakref.ref(obj)
    print(ref().value)
    del obj
    print(ref() is None)


if __name__ == "__main__":
    demo()
