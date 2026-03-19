"""
Memory multiprocessing_example6
multiprocessing_example6
"""
import multiprocessing


def worker(x):
    return x * 2


def demo():
    with multiprocessing.Pool(3) as p:
        results = p.map(worker, [1, 2, 3, 4])
        print(results)


if __name__ == "__main__":
    demo()
