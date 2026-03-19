"""
Memory concurrent_example2
concurrent_example2
"""
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def worker(x):
    return x * x


def demo():
    with ThreadPoolExecutor(max_workers=2) as p:
        print(list(p.map(worker, [1, 2, 3])))


if __name__ == "__main__":
    demo()
