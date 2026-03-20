"""
Memory queue_example18
queue_example18
"""
import queue


def demo():
    q = queue.Queue()
    q.put(1)
    print(q.qsize())


if __name__ == "__main__":
    demo()
