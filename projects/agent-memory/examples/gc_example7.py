"""
Memory gc_example7
gc_example7
"""
import gc


def demo():
    print(gc.get_referrers())


if __name__ == "__main__":
    demo()
