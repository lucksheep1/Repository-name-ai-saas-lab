"""
Memory queue_example11
queue_example11
"""
from queue import Queue


def demo():
    q = Queue()
    q.put("item1")
    q.put("item2")
    print(q.get_nowait())
    print(q.get_nowait())


if __name__ == "__main__":
    demo()
