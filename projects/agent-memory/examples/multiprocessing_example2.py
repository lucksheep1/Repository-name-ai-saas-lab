"""
Memory multiprocessing_example2
multiprocessing_example2
"""
import multiprocessing


def worker(x):
    return x * x


def demo():
    with multiprocessing.Pool(4) as p:
        results = p.map(worker, [1, 2, 3, 4])
        print(results)


if __name__ == "__main__":
    demo()
