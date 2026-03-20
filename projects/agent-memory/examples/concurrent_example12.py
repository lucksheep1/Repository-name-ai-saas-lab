"""
Memory concurrent_example12
concurrent_example12
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(worker, range(10)))
        print(results)


if __name__ == "__main__":
    demo()
