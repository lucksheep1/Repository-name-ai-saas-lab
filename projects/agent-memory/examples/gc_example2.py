"""
Memory gc_example2
gc_example2
"""
import gc


def demo():
    print(gc.get_count()[:3])


if __name__ == "__main__":
    demo()
