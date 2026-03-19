"""
Memory queue_example7
queue_example7
"""
from queue import Queue, Empty


def demo():
    q = Queue()
    q.put(1)
    q.put(2)
    print(q.get())
    print(q.qsize())


if __name__ == "__main__":
    demo()
