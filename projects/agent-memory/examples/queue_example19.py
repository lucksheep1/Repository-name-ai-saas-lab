"""
Memory queue_example19
queue_example19
"""
import queue


def demo():
    q = queue.Queue(maxsize=3)
    q.put(1)
    q.put(2)
    print(q.full())


if __name__ == "__main__":
    demo()
