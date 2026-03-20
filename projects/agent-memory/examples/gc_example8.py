"""
Memory gc_example8
gc_example8
"""
import gc


def demo():
    print(gc.get_objects()[:3])


if __name__ == "__main__":
    demo()
