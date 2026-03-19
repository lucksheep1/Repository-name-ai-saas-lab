"""
Memory multiprocessing
multiprocessing utilities
"""
from memory import Memory
import multiprocessing


def worker(x):
    return x * x


def demo():
    with multiprocessing.Pool(2) as pool:
        result = pool.map(worker, [1, 2, 3])
        print(result)


if __name__ == "__main__":
    demo()
