"""
Memory threading_example13
threading_example13
"""
import threading


def worker(n):
    print(f"Thread {n} started")


def demo():
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    demo()
