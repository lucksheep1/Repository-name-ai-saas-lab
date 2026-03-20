"""
Memory weakref_example6
weakref_example6
"""
import weakref


class A:
    pass


def demo():
    a = A()
    d = weakref.WeakValueDictionary()
    d["key"] = a
    print("done")


if __name__ == "__main__":
    demo()
