"""
Memory weakref_example11
weakref_example11
"""
import weakref


class MyClass:
    def __init__(self, value):
        self.value = value


def demo():
    obj = MyClass(100)
    ref = weakref.ref(obj)
    print(ref().value)


if __name__ == "__main__":
    demo()
