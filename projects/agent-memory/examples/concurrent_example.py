"""
Memory concurrent_example
concurrent_example
"""
from concurrent.futures import ThreadPoolExecutor


def worker(x):
    return x * x


def demo():
    with ThreadPoolExecutor(max_workers=2) as p:
        print(p.map(worker, [1, 2, 3]))


if __name__ == "__main__":
    demo()
