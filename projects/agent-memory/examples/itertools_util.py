"""
Memory itertools
itertools utilities
"""
import itertools


def demo():
    for i in itertools.islice(itertools.count(1), 5):
        print(i)


if __name__ == "__main__":
    demo()
