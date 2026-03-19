"""
Memory graphlib_example
graphlib_example
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("B", "A")
    ts.add("C", "B")
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
