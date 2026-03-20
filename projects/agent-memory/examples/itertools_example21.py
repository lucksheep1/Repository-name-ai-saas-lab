"""
Memory itertools_example21
itertools_example21
"""
import itertools


def demo():
    print(list(itertools.zip_longest([1, 2], ["a", "b", "c"])))


if __name__ == "__main__":
    demo()
