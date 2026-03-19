"""
Memory gc
gc utilities
"""
from memory import Memory
import gc


def demo():
    gc.collect()
    print("garbage collected")


if __name__ == "__main__":
    demo()
