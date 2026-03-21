"""
Memory functools_example25
functools_example25
"""
from functools import cmp_to_key


def cmp(a, b):
    return len(a) - len(b)


def demo():
    words = ["hi", "hello", "hey"]
    print(sorted(words, key=cmp_to_key(cmp)))


if __name__ == "__main__":
    demo()
