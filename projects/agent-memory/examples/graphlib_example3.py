"""
Memory graphlib_example3
graphlib_example3
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("D", "B", "C")
    ts.add("B", "A")
    ts.add("C", "A")
    order = list(ts.static_order())
    print(order)


if __name__ == "__main__":
    demo()
