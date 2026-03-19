"""
Memory concurrent_example8
concurrent_example8
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(worker, range(10)))
        print(results)


if __name__ == "__main__":
    demo()
