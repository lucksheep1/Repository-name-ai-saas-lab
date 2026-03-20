"""
Memory itertools_example14
itertools_example14
"""
import itertools


def demo():
    print(list(itertools.islice(itertools.count(10), 5)))


if __name__ == "__main__":
    demo()
