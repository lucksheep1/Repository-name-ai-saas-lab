"""
Memory queue_example10
queue_example10
"""
from queue import Queue


def demo():
    q = Queue()
    q.put("first")
    q.put("second")
    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    demo()
