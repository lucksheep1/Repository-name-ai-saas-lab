"""
Memory concurrent_example19
concurrent_example19
"""
import concurrent.futures


def worker(n):
    return n * 2


def demo():
    with concurrent.futures.ThreadPoolExecutor() as ex:
        f = ex.submit(worker, 10)
        print(f.result())


if __name__ == "__main__":
    demo()
