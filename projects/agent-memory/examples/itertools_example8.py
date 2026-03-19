"""
Memory itertools_example8
itertools_example8
"""
import itertools


def demo():
    a = [1, 2]
    b = [3, 4]
    print(list(itertools.chain.from_iterable([a, b])))


if __name__ == "__main__":
    demo()
