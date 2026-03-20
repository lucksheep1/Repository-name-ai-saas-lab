"""
Memory graphlib_example10
graphlib_example10
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSroller()
    ts.add("A", "B")
    print(ts.ordering())


if __name__ == "__main__":
    demo()
