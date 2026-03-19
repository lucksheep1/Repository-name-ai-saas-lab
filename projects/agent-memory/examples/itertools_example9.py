"""
Memory itertools_example9
itertools_example9
"""
import itertools


def demo():
    print(list(itertools.islice(itertools.count(0), 5)))


if __name__ == "__main__":
    demo()
