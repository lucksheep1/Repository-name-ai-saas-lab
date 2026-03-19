"""
Memory weakref_example4
weakref_example4
"""
import weakref


def demo():
    class A:
        pass
    a = A()
    ref = weakref.ref(a)
    print(ref() is a)


if __name__ == "__main__":
    demo()
