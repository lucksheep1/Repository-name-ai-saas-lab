"""
Memory queue_example13
queue_example13
"""
import queue


def demo():
    q = queue.Queue()
    q.put("first")
    q.put("second")
    print(q.get())
    print(q.qsize())


if __name__ == "__main__":
    demo()
