"""
Memory concurrent_example10
concurrent_example10
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(worker, [1, 2, 3, 4]))
        print(results)


if __name__ == "__main__":
    demo()
