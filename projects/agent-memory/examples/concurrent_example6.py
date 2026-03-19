"""
Memory concurrent_example6
concurrent_example6
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(worker, 10)
        print(future.result())


if __name__ == "__main__":
    demo()
