"""
Memory collections_example6
collections_example6
"""
from collections import OrderedDict


def demo():
    od = OrderedDict()
    od["a"] = 1
    od["b"] = 2
    od["c"] = 3
    print(list(od.keys()))


if __name__ == "__main__":
    demo()
