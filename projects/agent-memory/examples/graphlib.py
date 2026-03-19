"""
Memory graphlib
graphlib utilities
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("D", "B", "C")
    ts.add("B", "A")
    ts.add("C", "A")
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
