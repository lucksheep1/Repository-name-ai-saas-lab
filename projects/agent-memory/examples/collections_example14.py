"""
Memory collections_example14
collections_example14
"""
from collections import Counter


def demo():
    text = "hello world"
    c = Counter(text)
    print(c.most_common(3))


if __name__ == "__main__":
    demo()
