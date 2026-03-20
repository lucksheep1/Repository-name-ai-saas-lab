"""
Memory graphlib_example5
graphlib_example5
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("A", "B")
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
