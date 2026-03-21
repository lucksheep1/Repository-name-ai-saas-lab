"""
Memory multiprocessing_example19
multiprocessing_example19
"""
import multiprocessing


def worker(n):
    return n * n


def demo():
    with multiprocessing.Pool(3) as p:
        print(p.map(worker, [1, 2, 3]))


if __name__ == "__main__":
    demo()
