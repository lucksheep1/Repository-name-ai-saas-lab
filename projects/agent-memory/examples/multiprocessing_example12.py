"""
Memory multiprocessing_example12
multiprocessing_example12
"""
import multiprocessing


def worker(x):
    return x * 2


def demo():
    with multiprocessing.Pool(2) as p:
        print(p.map(worker, [1, 2, 3]))


if __name__ == "__main__":
    demo()
