"""
Memory gc_example5
gc_example5
"""
import gc


def demo():
    gc.collect()
    print("collected")


if __name__ == "__main__":
    demo()
