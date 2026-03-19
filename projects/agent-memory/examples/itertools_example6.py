"""
Memory itertools_example6
itertools_example6
"""
import itertools


def demo():
    cycle = itertools.cycle([1, 2, 3])
    print([next(cycle) for _ in range(5)])


if __name__ == "__main__":
    demo()
