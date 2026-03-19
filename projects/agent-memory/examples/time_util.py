"""
Memory Time
Time utilities
"""
from memory import Memory
import time


def demo():
    start = time.time()
    time.sleep(0.01)
    elapsed = time.time() - start
    print(elapsed)


if __name__ == "__main__":
    demo()
