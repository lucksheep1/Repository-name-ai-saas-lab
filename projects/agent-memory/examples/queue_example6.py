"""
Memory queue_example6
queue_example6
"""
from queue import Queue
import threading


def demo():
    q = Queue()
    q.put(1)
    q.put(2)
    q.put(3)
    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    demo()
