"""
Memory collections_example18
collections_example18
"""
from collections import Counter


def demo():
    c = Counter("hello")
    print(c.most_common(1))


if __name__ == "__main__":
    demo()
