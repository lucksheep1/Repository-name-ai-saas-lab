"""
Memory collections_example5
collections_example5
"""
from collections import Counter


def demo():
    text = "hello world"
    counter = Counter(text)
    print(counter.most_common(3))


if __name__ == "__main__":
    demo()
