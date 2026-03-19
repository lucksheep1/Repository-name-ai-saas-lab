"""
Memory queue_example4
queue_example4
"""
from queue import Queue, Empty


def demo():
    q = Queue()
    q.put(1)
    q.put(2)
    try:
        item = q.get_nowait()
        print(item)
    except Empty:
        print("empty")


if __name__ == "__main__":
    demo()
