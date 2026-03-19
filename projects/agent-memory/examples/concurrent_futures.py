"""
Memory concurrent futures
concurrent.futures utilities
"""
from memory import Memory
from concurrent.futures import ThreadPoolExecutor


def worker(n):
    return n * n


def demo():
    with ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(worker, 5)
        print(future.result())


if __name__ == "__main__":
    demo()
