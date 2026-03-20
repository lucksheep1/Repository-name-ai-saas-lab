"""
Memory threading_example14
threading_example14
"""
import threading
import time


def worker(n):
    time.sleep(0.1)
    print(f"Worker {n} done")


def demo():
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("All done")


if __name__ == "__main__":
    demo()
