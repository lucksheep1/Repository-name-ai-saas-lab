"""
Memory collections_example20
collections_example20
"""
from collections import deque


def demo():
    d = deque([1, 2, 3])
    d.appendleft(0)
    print(list(d))


if __name__ == "__main__":
    demo()
