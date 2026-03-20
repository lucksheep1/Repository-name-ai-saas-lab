"""
Memory concurrent_example13
concurrent_example13
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(worker, i) for i in range(5)]
        for f in concurrent.futures.as_completed(futures):
            print(f.result())


if __name__ == "__main__":
    demo()
