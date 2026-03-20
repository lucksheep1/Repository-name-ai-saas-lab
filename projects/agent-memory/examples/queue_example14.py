"""
Memory queue_example14
queue_example14
"""
import queue


def demo():
    q = queue.LifoQueue()
    q.put(1)
    q.put(2)
    print(q.get())


if __name__ == "__main__":
    demo()
