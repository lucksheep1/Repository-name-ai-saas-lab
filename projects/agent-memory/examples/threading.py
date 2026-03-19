"""
Memory threading
threading utilities
"""
from memory import Memory
import threading


def worker():
    print("working")


def demo():
    t = threading.Thread(target=worker)
    t.start()
    t.join()


if __name__ == "__main__":
    demo()
