"""
Memory graphlib_example2
graphlib_example2
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("A", "B", "C")
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
