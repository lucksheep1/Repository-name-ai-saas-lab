"""
Memory collections_example13
collections_example13
"""
from collections import OrderedDict


def demo():
    d = OrderedDict()
    d["first"] = 1
    d["second"] = 2
    print(list(d.keys()))


if __name__ == "__main__":
    demo()
