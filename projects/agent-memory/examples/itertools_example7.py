"""
Memory itertools_example7
itertools_example7
"""
import itertools


def demo():
    a = [1, 2]
    b = ["a", "b"]
    print(list(itertools.product(a, b)))


if __name__ == "__main__":
    demo()
