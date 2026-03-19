"""
Memory collections_example7
collections_example7
"""
from collections import defaultdict


def demo():
    d = defaultdict(int)
    for char in "hello":
        d[char] += 1
    print(dict(d))


if __name__ == "__main__":
    demo()
