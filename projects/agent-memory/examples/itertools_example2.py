"""
Memory itertools_example2
itertools_example2
"""
import itertools


def demo():
    print(list(itertools.islice(itertools.count(10), 3)))


if __name__ == "__main__":
    demo()
