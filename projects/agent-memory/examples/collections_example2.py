"""
Memory collections_example2
collections_example2
"""
from collections import defaultdict, OrderedDict


def demo():
    d = defaultdict(list)
    d["key"].append("value")
    print(dict(d))


if __name__ == "__main__":
    demo()
