"""
Memory itertools_example25
itertools_example25
"""
import itertools


def demo():
    print(list(itertools.islice(itertools.count(10), 5)))


if __name__ == "__main__":
    demo()
