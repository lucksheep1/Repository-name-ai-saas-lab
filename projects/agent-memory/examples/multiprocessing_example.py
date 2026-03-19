"""
Memory multiprocessing_example
multiprocessing_example
"""
import multiprocessing


def worker(x):
    return x * x


def demo():
    with multiprocessing.Pool(2) as p:
        print(p.map(worker, [1, 2, 3]))


if __name__ == "__main__":
    demo()
