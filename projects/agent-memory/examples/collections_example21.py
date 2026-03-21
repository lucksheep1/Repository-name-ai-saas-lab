"""
Memory collections_example21
collections_example21
"""
from collections import Counter


def demo():
    c = Counter("hello")
    print(c.most_common())


if __name__ == "__main__":
    demo()
