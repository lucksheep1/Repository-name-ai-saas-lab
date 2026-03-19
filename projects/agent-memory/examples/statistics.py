"""
Memory Statistics
Statistics utilities
"""
from memory import Memory
import statistics


def demo():
    data = [1, 2, 3, 4, 5]
    print(statistics.mean(data))
    print(statistics.median(data))
    print(statistics.stdev(data))


if __name__ == "__main__":
    demo()
