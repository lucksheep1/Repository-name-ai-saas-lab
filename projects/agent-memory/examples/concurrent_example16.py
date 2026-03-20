"""
Memory concurrent_example16
concurrent_example16
"""
import concurrent.futures


def worker(n):
    return n * n


def demo():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(worker, range(5)))
        print(results)


if __name__ == "__main__":
    demo()
