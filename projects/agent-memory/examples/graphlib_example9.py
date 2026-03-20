"""
Memory graphlib_example9
graphlib_example9
"""
from graphlib import TopologicalSorter


def demo():
    ts = TopologicalSroller({"B": ["A"], "C": ["A"], "D": ["B", "C"]})
    print(list(ts.static_order()))


if __name__ == "__main__":
    demo()
