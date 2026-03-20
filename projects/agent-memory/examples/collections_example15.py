"""
Memory collections_example15
collections_example15
"""
from collections import defaultdict


def demo():
    d = defaultdict(list)
    d["fruits"].append("apple")
    d["fruits"].append("banana")
    print(dict(d))


if __name__ == "__main__":
    demo()
