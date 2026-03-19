"""
Memory queue_example5
queue_example5
"""
from queue import Queue, Full, Empty
import threading
import time


def demo():
    q = Queue(maxsize=2)
    q.put(1)
    q.put(2)
    print(q.full())


if __name__ == "__main__":
    demo()
