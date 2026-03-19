"""
Memory collections_example8
collections_example8
"""
from collections import Counter


def demo():
    text = "hello world hello"
    c = Counter(text.split())
    print(c)


if __name__ == "__main__":
    demo()
