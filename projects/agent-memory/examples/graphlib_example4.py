"""
Memory graphlib_example4
graphlib_example4
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("D", "C", "B", "A")
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
