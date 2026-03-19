"""
Memory queue_example2
queue_example2
"""
from queue import Queue


def demo():
    q = Queue()
    q.put(1)
    q.put(2)
    print(q.get())
    print(q.qsize())


if __name__ == "__main__":
    demo()
