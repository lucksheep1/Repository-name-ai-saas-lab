"""
Memory concurrent_example9
concurrent_example9
"""
import concurrent.futures


def demo():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future = executor.submit(pow, 2, 3)
        print(future.result())


if __name__ == "__main__":
    demo()
