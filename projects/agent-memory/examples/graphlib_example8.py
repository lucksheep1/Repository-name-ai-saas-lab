"""
Memory graphlib_example8
graphlib_example8
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSorter()
    ts.add("C", "B", "A")
    print(list(ts.ordering()))


if __name__ == "__main__":
    demo()
