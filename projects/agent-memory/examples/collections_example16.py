"""
Memory collections_example16
collections_example16
"""
from collections import deque


def demo():
    d = deque([1, 2, 3])
    d.appendleft(0)
    d.append(4)
    print(list(d))


if __name__ == "__main__":
    demo()
