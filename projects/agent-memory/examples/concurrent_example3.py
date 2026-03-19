"""
Memory concurrent_example3
concurrent_example3
"""
from concurrent.futures import as_completed


def worker(n):
    return n * n


def demo():
    with as_completed([worker(i) for i in range(3)]) as f:
        for result in f:
            print(result)


if __name__ == "__main__":
    demo()
