"""
Memory collections_example9
collections_example9
"""
from collections import deque


def demo():
    d = deque([1, 2, 3])
    d.appendleft(0)
    print(list(d))


if __name__ == "__main__":
    demo()
