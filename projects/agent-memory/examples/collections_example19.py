"""
Memory collections_example19
collections_example19
"""
from collections import defaultdict


def demo():
    d = defaultdict(int)
    d["a"] += 1
    print(dict(d))


if __name__ == "__main__":
    demo()
