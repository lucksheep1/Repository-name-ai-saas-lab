"""
Memory concurrent_example14
concurrent_example14
"""
import concurrent.futures


def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)


def demo():
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        future = executor.submit(fib, 10)
        print(f"Fib(10) = {future.result()}")


if __name__ == "__main__":
    demo()
