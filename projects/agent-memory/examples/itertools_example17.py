"""
Memory itertools_example17
itertools_example17
"""
import itertools


def demo():
    cycles = list(itertools.cycle([1, 2, 3]))
    print(cycles[:7])


if __name__ == "__main__":
    demo()
