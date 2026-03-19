"""
Memory concurrent_example7
concurrent_example7
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(worker, range(5)))
        print(results)


if __name__ == "__main__":
    demo()
