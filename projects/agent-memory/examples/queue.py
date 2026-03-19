"""
Memory queue
queue utilities
"""
from queue import Queue


def demo():
    q = Queue()
    q.put(1)
    print(q.get())


if __name__ == "__main__":
    demo()
