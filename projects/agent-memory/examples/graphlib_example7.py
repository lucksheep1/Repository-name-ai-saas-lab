"""
Memory graphlib_example7
graphlib_example7
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("D", "C", "B", "A")
    print(list(ts.ordering()))


if __name__ == "__main__":
    demo()
