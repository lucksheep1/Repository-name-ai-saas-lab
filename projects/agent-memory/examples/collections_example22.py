"""
Memory collections_example22
collections_example22
"""
from collections import OrderedDict


def demo():
    d = OrderedDict()
    d["a"] = 1
    d["b"] = 2
    d.move_to_end("a")
    print(list(d.keys()))


if __name__ == "__main__":
    demo()
