"""
Memory weakref_example8
weakref_example8
"""
import weakref


class MyClass:
    def __init__(self, value):
        self.value = value


def demo():
    obj = MyClass(42)
    ref = weakref.ref(obj)
    print(ref().value)


if __name__ == "__main__":
    demo()
