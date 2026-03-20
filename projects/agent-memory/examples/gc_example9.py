"""
Memory gc_example9
gc_example9
"""
import gc


def demo():
    gc.collect()
    print(f"Garbage objects: {len(gc.garbage)}")


if __name__ == "__main__":
    demo()
