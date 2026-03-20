"""
Memory collections_example10
collections_example10
"""
from collections import ChainMap


def demo():
    d1 = {"a": 1}
    d2 = {"b": 2}
    cm = ChainMap(d1, d2)
    print(cm["a"], cm["b"])


if __name__ == "__main__":
    demo()
