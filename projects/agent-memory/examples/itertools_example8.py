"""
Memory itertools_example8
itertools_example8
"""
import itertools


def demo():
    print(list(itertools.islice(itertools.count(1), 5)))


if __name__ == "__main__":
    demo()
