"""
Memory concurrent_example20
concurrent_example20
"""
import concurrent.futures


def worker(n):
    return n + 1


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(worker, [1, 2, 3]))
        print(results)


if __name__ == "__main__":
    demo()
