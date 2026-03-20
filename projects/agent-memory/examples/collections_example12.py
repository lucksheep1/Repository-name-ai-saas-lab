"""
Memory collections_example12
collections_example12
"""
from collections import Counter


def demo():
    c = Counter("hello world")
    print(c.most_common(3))


if __name__ == "__main__":
    demo()
