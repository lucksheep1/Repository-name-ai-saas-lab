"""
Memory queue_example16
queue_example16
"""
import queue


def demo():
    q = queue.Queue(maxsize=3)
    q.put(1)
    q.put(2)
    q.put(3)
    print(q.full())


if __name__ == "__main__":
    demo()
