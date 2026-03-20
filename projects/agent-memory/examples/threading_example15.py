"""
Memory threading_example15
threading_example15
"""
import threading
import time


def worker(msg):
    print(f"Worker: {msg}")


def demo():
    t = threading.Thread(target=worker, args=("Hello",))
    t.start()
    t.join()


if __name__ == "__main__":
    demo()
