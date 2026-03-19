"""
Memory Itertools
Itertools utilities
"""
from memory import Memory
import itertools


def demo():
    for i in itertools.count(5):
        if i > 7:
            break
        print(i)
    
    for i in itertools.repeat("x", 3):
        print(i)
    
    for i in itertools.chain([1, 2], [3, 4]):
        print(i)


if __name__ == "__main__":
    demo()
