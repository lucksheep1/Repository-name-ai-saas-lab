"""
Memory gc_example11
gc_example11
"""
import gc


def demo():
    gc.collect()
    print(gc.get_count())


if __name__ == "__main__":
    demo()
