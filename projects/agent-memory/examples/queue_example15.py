"""
Memory queue_example15
queue_example15
"""
import queue


def demo():
    q = queue.Queue()
    q.put(1)
    print(q.get())


if __name__ == "__main__":
    demo()
