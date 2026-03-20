"""
Memory gc_example10
gc_example10
"""
import gc


class MyObject:
    pass


def demo():
    obj = MyObject()
    gc.collect()
    print(gc.get_count())


if __name__ == "__main__":
    demo()
