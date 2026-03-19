"""
Memory Random
Random utilities
"""
from memory import Memory
import random


def demo():
    print(random.randint(1, 100))
    print(random.choice(["a", "b", "c"]))
    random.shuffle([1, 2, 3])


if __name__ == "__main__":
    demo()
