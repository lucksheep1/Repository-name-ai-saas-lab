"""
Memory gc_example
gc_example
"""
import gc


def demo():
    gc.collect()
    print("gc done")


if __name__ == "__main__":
    demo()
