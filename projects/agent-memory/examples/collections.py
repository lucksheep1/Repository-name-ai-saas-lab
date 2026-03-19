"""
Memory Collections
Collections utilities
"""
from memory import Memory
from collections import Counter, defaultdict, OrderedDict


def demo():
    c = Counter(["a", "b", "a"])
    print(c)
    
    d = defaultdict(int)
    d["key"] += 1
    print(d)


if __name__ == "__main__":
    demo()
