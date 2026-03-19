"""
Memory concurrent_example5
concurrent_example5
"""
from concurrent.futures import ThreadPoolExecutor


def worker(n):
    return n * n


def demo():
    with ThreadPoolExecutor(max_workers=4) as executor:
        future = executor.submit(worker, 5)
        print(future.result())


if __name__ == "__main__":
    demo()
