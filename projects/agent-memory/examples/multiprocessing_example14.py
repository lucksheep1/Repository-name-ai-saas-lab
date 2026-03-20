"""
Memory multiprocessing_example14
multiprocessing_example14
"""
import multiprocessing


def worker(x):
    return x * x


def demo():
    with multiprocessing.Pool(4) as pool:
        result = pool.map(worker, [1, 2, 3, 4, 5])
        print(result)


if __name__ == "__main__":
    demo()
