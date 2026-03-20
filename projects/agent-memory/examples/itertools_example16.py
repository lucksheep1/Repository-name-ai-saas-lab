"""
Memory itertools_example16
itertools_example16
"""
import itertools


def demo():
    a = [1, 2]
    b = ['a', 'b']
    print(list(itertools.product(a, b)))


if __name__ == "__main__":
    demo()
